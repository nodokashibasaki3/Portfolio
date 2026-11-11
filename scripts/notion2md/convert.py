"""Convert a Notion page's blocks into plain Markdown for this Jekyll site.

Posts keep formatting out of the Markdown (see README "Blog posts"):
- link previews become `{% include card.html url="..." %}`; their details are collected in
  `Converter.previews` for _data/link_previews.json
- callouts become quotes tagged `{: .callout}`, styled by assets/css/blog.css
"""

from __future__ import annotations

import logging
import re
import urllib.parse
from collections.abc import Callable
from typing import Any, Protocol

from .local_cache import LocalCache
from .rich_text import Mark, escape_pipes, plain_text, to_html, to_markdown

log = logging.getLogger(__name__)

Block = dict[str, Any]

HEADING_MARKS = {"header": "##", "sub_header": "###", "sub_sub_header": "####"}
LIST_MARKS = {"bulleted_list": "-", "numbered_list": "1."}
LINK_TYPES = {"bookmark", "external_object_instance", "embed", "video", "file", "pdf"}
CARD_TYPES = {"bookmark", "external_object_instance"}
PASSTHROUGH_TYPES = {"column_list", "column", "transclusion_container"}  # render children only
SKIPPED_TYPES = {"table_of_contents"}

# A heading that is only a greeting word plus punctuation/emoji, e.g. "hey 👋" or "hello."
GREETING = re.compile(r"^(?:hey|hello|hi)\b[\W_]*$")
# An opening "i'm nodoka ..." / "I am [Nodoka Shibasaki](...) ..." sentence: up to the first
# . ! or ? followed by a space or the end (so a period inside a link URL doesn't end it).
SELF_INTRO = re.compile(r"^i(?:['’]m| am)\s+\[?nodoka\b.*?(?:[.!?](?=\s|$)|$)\s*", re.IGNORECASE)
# Titles Notion saves when a site shows a bot check instead of the real page.
BOT_CHECK_TITLES = ("establishing a secure connection", "just a moment", "attention required")
UNRESOLVED_LINK = "[link?]"
UNRESOLVED_PERSON = "[person?]"
INDENT = "   "  # 3 spaces: content under "1. " must line up with its text, not just "- "


class PageLookup(Protocol):
    def page_title(self, page_id: str) -> str | None: ...
    def page_url(self, page_id: str) -> str: ...
    def image_url(self, block: Block) -> str: ...


def liquid_str(value: str) -> str:
    """Make a value safe inside a double-quoted Liquid include parameter."""
    escaped = value.replace('"', "&quot;").replace("{", "&#123;").replace("}", "&#125;")
    return escaped.strip()


def domain_of(url: str) -> str:
    return urllib.parse.urlparse(url).netloc


def drop_self_intro(paragraph: str) -> str:
    """Remove an opening "I'm Nodoka..." sentence; returns "" if nothing else is left."""
    return SELF_INTRO.sub("", paragraph, count=1).strip()


def link_preview(block: Block, url: str) -> dict[str, str]:
    """Title, description, icon, and thumbnail Notion saved for a bookmark (empty fields dropped)."""
    props, fmt = block.get("properties", {}), block.get("format", {})
    title, description = plain_text(props.get("title")), plain_text(props.get("description"))
    if title.lower().startswith(BOT_CHECK_TITLES):
        title, description = domain_of(url).removeprefix("www."), ""
    preview = {
        "title": title.strip(),
        "description": description.strip(),
        "image": fmt.get("bookmark_cover", ""),
        "icon": fmt.get("bookmark_icon", ""),
    }
    return {key: value for key, value in preview.items() if value}


class Converter:
    """Renders one page. Create a new Converter per page.

    After convert(), `previews` maps each card URL to its preview details, for
    _data/link_previews.json.
    """

    def __init__(self, blocks: dict[str, Block], cache: LocalCache, pages: PageLookup) -> None:
        self.blocks = blocks
        self.cache = cache
        self.pages = pages
        self.previews: dict[str, dict[str, str]] = {}
        self._handlers: dict[str, Callable[[Block, int], list[str]]] = {
            **{kind: self._heading for kind in HEADING_MARKS},
            **{kind: self._list_item for kind in LIST_MARKS},
            **{kind: self._link_block for kind in LINK_TYPES},
            "text": self._paragraph,
            "to_do": self._to_do,
            "toggle": self._toggle,
            "quote": self._quote,
            "callout": self._callout,
            "code": self._code,
            "divider": lambda block, depth: ["---"],
            "image": self._image,
            "equation": self._equation,
            "table": self._table,
            "page": self._child_page,
            "alias": self._alias,
        }

    def convert(self, page_id: str) -> str:
        """Markdown body for the page, without its title."""
        children = self.blocks[page_id].get("content") or []
        if children and self._is_greeting(self.blocks.get(children[0], {})):
            children = children[1:]
        lines = [line for child in children for line in self.render(child, 0) if line.strip()]
        if lines:
            lines = [drop_self_intro(lines[0]), *lines[1:]]
        return tidy("\n\n".join(line for line in lines if line))

    def page_title(self, page_id: str) -> str:
        return self._text(self.blocks[page_id])

    def render(self, block_id: str, depth: int) -> list[str]:
        block = self.blocks.get(block_id)
        if block is None:
            log.warning("block %s is missing from the page data", block_id)
            return []
        kind = block.get("type", "")
        if kind in PASSTHROUGH_TYPES:
            return self._children(block, depth)
        if kind in SKIPPED_TYPES:
            return []
        handler = self._handlers.get(kind)
        if handler is None:
            log.warning("unsupported block type %r; left as an HTML comment", kind)
            return [f"<!-- unsupported Notion block: {kind} -->"]
        return handler(block, depth)

    # --- helpers -------------------------------------------------------------------------

    def _children(self, block: Block, depth: int) -> list[str]:
        return [line for child in block.get("content") or [] for line in self.render(child, depth)]

    def _text(self, block: Block, key: str = "title") -> str:
        return to_markdown(block.get("properties", {}).get(key), self._mention)

    def _mention(self, mark: Mark) -> str:
        kind, value = mark[0], mark[1] if len(mark) > 1 else None
        if kind == "lm":
            return f"[{escape_pipes(value.get('title') or value['href'])}]({value['href']})"
        if kind == "d":
            return value.get("start_date", "")
        if kind == "u":
            return self._person(value)
        if kind == "p":
            title = escape_pipes(self.pages.page_title(value) or "notion page")
            return f"[{title}]({self.pages.page_url(value)})"
        if kind == "eoi" and value in self.cache.link_urls:
            url = self.cache.link_urls[value]
            return f"[{url.rstrip('/').split('/')[-1] or url}]({url})"
        log.warning("unresolved inline mention %r", mark)
        return UNRESOLVED_LINK

    def _person(self, user_id: str) -> str:
        name = self.cache.user_names.get(user_id)
        if not name:
            log.warning("no name for mentioned user %s (is the Notion app cache available?)", user_id)
        return name or UNRESOLVED_PERSON

    def _block_url(self, block: Block) -> str | None:
        if block.get("type") == "external_object_instance":
            return self.cache.link_urls.get(block.get("id", ""))
        props = block.get("properties", {})
        url = plain_text(props.get("link") or props.get("source"))
        return url if url.startswith("http") else None

    def _is_greeting(self, block: Block) -> bool:
        """An opening heading like 'hey 👋' or 'hello.'"""
        if block.get("type") not in HEADING_MARKS:
            return False
        return bool(GREETING.match(self._text(block).lower().strip()))

    # --- block handlers ------------------------------------------------------------------

    def _heading(self, block: Block, depth: int) -> list[str]:
        return [f"{HEADING_MARKS[block['type']]} {self._text(block)}", *self._children(block, depth)]

    def _paragraph(self, block: Block, depth: int) -> list[str]:
        return [f"{INDENT * depth}{self._text(block)}", *self._children(block, depth + 1)]

    def _list_item(self, block: Block, depth: int) -> list[str]:
        mark = LIST_MARKS[block["type"]]
        return [f"{INDENT * depth}{mark} {self._text(block)}", *self._children(block, depth + 1)]

    def _to_do(self, block: Block, depth: int) -> list[str]:
        checked = plain_text(block.get("properties", {}).get("checked")) == "Yes"
        box = "x" if checked else " "
        return [f"{INDENT * depth}- [{box}] {self._text(block)}", *self._children(block, depth + 1)]

    def _toggle(self, block: Block, depth: int) -> list[str]:
        summary = to_html(block.get("properties", {}).get("title"))
        ind = INDENT * depth
        return [
            f'{ind}<details markdown="1"><summary>{summary}</summary>\n',
            *self._children(block, depth),
            f"{ind}</details>",
        ]

    def _quote(self, block: Block, depth: int) -> list[str]:
        text = self._text(block)
        parts = ([text] if text else []) + self._children(block, 0)
        return ["\n".join(self._quoted(parts, depth))] if parts else []

    @staticmethod
    def _quoted(parts: list[str], depth: int) -> list[str]:
        """Prefix every line with "> " so the quote's text and nested blocks form one quote."""
        ind = INDENT * depth
        body = tidy("\n\n".join(parts)).rstrip("\n")  # tidy before quoting, so lists stay tight
        return [f"{ind}>" if not line else f"{ind}> {line}" for line in body.split("\n")]

    def _callout(self, block: Block, depth: int) -> list[str]:
        """A quote tagged {: .callout}, which assets/css/blog.css draws as a gray box."""
        link_only = self._is_link_only(block)
        text = self._text(block)
        emoji = block.get("format", {}).get("page_icon", "")
        if emoji.startswith(("http", "/")) or link_only:  # custom image icons; cards have their own
            emoji = ""
        parts = ([text] if text else []) + self._children(block, 0)
        if emoji:  # lead with the emoji, whether the text is the callout's own or nested
            parts = [f"{emoji} {parts[0]}" if parts else emoji, *parts[1:]]
        classes = ".callout .callout-link" if link_only else ".callout"
        # One entry, so no blank line separates the quote from the tag that styles it.
        return ["\n".join([*self._quoted(parts, depth), f"{INDENT * depth}{{: {classes}}}"])]

    def _is_link_only(self, block: Block) -> bool:
        children = block.get("content") or []
        return (
            bool(children)
            and not self._text(block)
            and all(self.blocks.get(child, {}).get("type") in LINK_TYPES for child in children)
        )

    def _code(self, block: Block, depth: int) -> list[str]:
        props = block.get("properties", {})
        language = plain_text(props.get("language")).lower()
        ind = INDENT * depth
        return [f"{ind}```{language}\n{plain_text(props.get('title'))}\n{ind}```"]

    def _image(self, block: Block, depth: int) -> list[str]:
        caption_md = self._text(block, "caption")
        alt = plain_text(block.get("properties", {}).get("caption")).replace("[", "").replace("]", "")
        ind = INDENT * depth
        lines = [f"{ind}![{alt}]({self.pages.image_url(block)})"]
        if caption_md and caption_md != alt:  # keep links/formatting from the caption visible
            lines.append(f"{ind}*{caption_md}*")
        return lines

    def _link_block(self, block: Block, depth: int) -> list[str]:
        ind = INDENT * depth
        url = self._block_url(block)
        if not url:
            log.warning("no URL for %s block %s", block.get("type"), block.get("id"))
            return [f"{ind}{UNRESOLVED_LINK}"]
        if block["type"] in CARD_TYPES:
            return [f"{ind}{self._card(block, url)}"]
        label = self._text(block) or self._text(block, "caption") or url
        return [f"{ind}[{label}]({url})"]

    def _card(self, block: Block, url: str) -> str:
        """A one-line card include; its preview details go to self.previews, not the post."""
        if not domain_of(url).endswith("github.com"):
            preview = link_preview(block, url)
            if preview:
                self.previews[url] = preview
        return f'{{% include card.html url="{liquid_str(url)}" %}}'

    def _equation(self, block: Block, depth: int) -> list[str]:
        return [f"$$\n{plain_text(block.get('properties', {}).get('title'))}\n$$"]

    def _table(self, block: Block, depth: int) -> list[str]:
        columns = block.get("format", {}).get("table_block_column_order", [])
        rows = [
            "| " + " | ".join(self._text(self.blocks.get(row, {}), col) for col in columns) + " |"
            for row in block.get("content") or []
        ]
        return [rows[0], "|" + "---|" * len(columns), *rows[1:]] if rows else []

    def _child_page(self, block: Block, depth: int) -> list[str]:
        title = self._text(block) or "notion page"
        return [f"{INDENT * depth}- [{title}]({self.pages.page_url(block['id'])})"]

    def _alias(self, block: Block, depth: int) -> list[str]:
        target = block.get("format", {}).get("alias_pointer", {}).get("id", "")
        if not target:
            return []
        title = self.pages.page_title(target) or "notion page"
        return [f"{INDENT * depth}[{title}]({self.pages.page_url(target)})"]


LIST_LINE = re.compile(r"^\s*(?:[-*]|\d+\.)\s")
HEADING_LINE = re.compile(r"^#{1,6}\s")


def tidy(markdown: str) -> str:
    """Collapse blank runs, keep lists tight, and drop dividers right under headings."""
    lines = markdown.split("\n")
    out: list[str] = []

    def last_text_line() -> str:
        return next((line for line in reversed(out) if line.strip()), "")

    for i, line in enumerate(lines):
        if not line.strip():
            following = next((nxt for nxt in lines[i + 1 :] if nxt.strip()), "")
            # Only list item -> list item stays tight; a paragraph or card under an item keeps
            # its blank line, or Markdown would merge it into the item's text.
            between_items = LIST_LINE.match(last_text_line()) and LIST_LINE.match(following)
            if between_items or (out and not out[-1].strip()):
                continue
        elif line.strip() == "---" and HEADING_LINE.match(last_text_line()):
            continue
        out.append(line.rstrip())
    return "\n".join(out).strip() + "\n"
