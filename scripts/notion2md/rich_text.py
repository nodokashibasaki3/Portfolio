"""Convert Notion rich text (lists of [text, [format, ...]] segments) to Markdown or HTML."""

from __future__ import annotations

import html
from collections.abc import Callable
from typing import Any

Segment = list[Any]  # [text] or [text, [[mark, arg?], ...]]
Mark = list[Any]

MENTION_CHAR = "‣"  # Notion's placeholder text for an inline mention
MARKDOWN_MARKS = {"b": "**{}**", "i": "*{}*", "c": "`{}`", "s": "~~{}~~"}
HTML_TAGS = {"b": "strong", "i": "em", "c": "code", "s": "del"}


def _marks(segment: Segment) -> list[Mark]:
    return segment[1] if len(segment) > 1 else []


def plain_text(segments: list[Segment] | None) -> str:
    return "".join(segment[0] for segment in segments or [])


def to_markdown(segments: list[Segment] | None, mention: Callable[[Mark], str]) -> str:
    """Render rich text as Markdown; `mention` renders inline mentions (people, pages, links)."""
    out = []
    for segment in segments or []:
        text, marks = segment[0], _marks(segment)
        if text == MENTION_CHAR and marks:
            out.append(mention(marks[0]))
            continue
        for mark in marks:
            if mark[0] in MARKDOWN_MARKS:
                text = MARKDOWN_MARKS[mark[0]].format(text)
            elif mark[0] == "a":
                text = f"[{text}]({mark[1]})"
        out.append(text)
    return "".join(out)


def to_html(segments: list[Segment] | None) -> str:
    """Render rich text as inline HTML, for places Markdown isn't parsed (e.g. <summary>)."""
    out = []
    for segment in segments or []:
        text = html.escape(segment[0])
        for mark in _marks(segment):
            tag = HTML_TAGS.get(mark[0])
            if tag:
                text = f"<{tag}>{text}</{tag}>"
        out.append(text)
    return "".join(out).strip()


def first_url(segments: list[Segment] | None, link_urls: dict[str, str]) -> str | None:
    """First http(s) URL in rich text: plain links, link mentions, or cached link previews."""
    for segment in segments or []:
        for mark in _marks(segment):
            kind = mark[0]
            if kind == "a" and str(mark[1]).startswith("http"):
                return mark[1]
            if kind == "lm":
                return mark[1].get("href")
            if kind == "eoi" and mark[1] in link_urls:
                return link_urls[mark[1]]
    return None
