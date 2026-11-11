"""Unit tests for the Notion -> Markdown conversion (no network).

Run from the repo root: python3 -m unittest scripts.notion2md.test_convert
"""

from __future__ import annotations

import unittest
from typing import Any

from .convert import Converter, liquid_str, tidy
from .links import rewrite_post_links
from .local_cache import LocalCache
from .rich_text import plain_text, to_html, to_markdown

PAGE = "page"


class FakePages:
    def page_title(self, page_id: str) -> str | None:
        return {"other": "my macos I"}.get(page_id)

    def page_url(self, page_id: str) -> str:
        return f"https://example.notion.site/{page_id}"

    def image_url(self, block: dict[str, Any]) -> str:
        return f"https://img/{block['id']}"


def block(block_id: str, kind: str, title: str | None = None, content=(), **extra) -> dict:
    props = dict(extra.pop("properties", {}))
    if title is not None:
        props["title"] = [[title]]
    return {"id": block_id, "type": kind, "properties": props, "content": list(content), **extra}


def converter_for(*children: dict, cache: LocalCache | None = None) -> Converter:
    blocks = {child["id"]: child for child in children}
    top_level = [c["id"] for c in children if not c.get("nested")]
    blocks[PAGE] = block(PAGE, "page", "Post", top_level)
    return Converter(blocks, cache or LocalCache(), FakePages())


def convert(*children: dict, cache: LocalCache | None = None) -> str:
    return converter_for(*children, cache=cache).convert(PAGE)


class RichTextTest(unittest.TestCase):
    def test_marks_render_as_markdown(self):
        segments = [["bold", [["b"]]], [" and "], ["code", [["c"]]], [" "], ["link", [["a", "https://x.y"]]]]
        self.assertEqual(to_markdown(segments, str), "**bold** and `code` [link](https://x.y)")

    def test_mentions_use_the_mention_renderer(self):
        segments = [["‣", [["u", "user-1"]]]]
        self.assertEqual(to_markdown(segments, lambda mark: f"<{mark[1]}>"), "<user-1>")

    def test_html_escapes_text(self):
        self.assertEqual(to_html([["a < b", [["b"]]]]), "<strong>a &lt; b</strong>")

    def test_plain_text_ignores_marks(self):
        self.assertEqual(plain_text([["a", [["b"]]], ["b"]]), "ab")


class MarkdownEdgeCaseTest(unittest.TestCase):
    def test_spaces_stay_outside_emphasis(self):
        segments = [["built by "], ["Mikker ", [["b"]]], ["also"]]
        self.assertEqual(to_markdown(segments, str), "built by **Mikker** also")

    def test_neighbors_with_the_same_marks_merge(self):
        segments = [["Side Note: ", [["b"]]], ["Apple Calendar", [["b"]]]]
        self.assertEqual(to_markdown(segments, str), "**Side Note: Apple Calendar**")

    def test_whitespace_only_marked_text_is_left_plain(self):
        self.assertEqual(to_markdown([["a"], ["  ", [["b"]]], ["b"]], str), "a  b")

    def test_code_is_the_innermost_mark(self):
        segments = [["ollama", [["b"], ["c"]]], [" "], ["q", [["a", "https://g.co"], ["c"]]]]
        self.assertEqual(to_markdown(segments, str), "**`ollama`** [`q`](https://g.co)")

    def test_pipes_are_escaped_outside_code(self):
        segments = [["Emoji | Raycast", [["a", "https://r.co"]]], [" "], ["a|b", [["c"]]]]
        self.assertEqual(to_markdown(segments, str), "[Emoji \\| Raycast](https://r.co) `a|b`")


class ConvertTest(unittest.TestCase):
    def test_opening_greeting_heading_is_dropped(self):
        md = convert(block("h", "header", "hey 👋"), block("t", "text", "hi there"))
        self.assertEqual(md, "hi there\n")

    def test_heading_that_only_starts_with_hi_is_kept(self):
        md = convert(block("h", "header", "highlights"))
        self.assertEqual(md, "## highlights\n")

    def test_mentioned_people_use_cached_names(self):
        text = block("t", "text", properties={"title": [["by "], ["‣", [["u", "u1"]]]]})
        self.assertEqual(convert(text, cache=LocalCache(user_names={"u1": "Alan Huang"})), "by Alan Huang\n")

    def test_unknown_person_gets_a_visible_placeholder(self):
        text = block("t", "text", properties={"title": [["‣", [["u", "u1"]]]]})
        with self.assertLogs(level="WARNING"):
            self.assertEqual(convert(text), "[person?]\n")

    def test_page_mentions_link_to_the_page(self):
        text = block("t", "text", properties={"title": [["‣", [["p", "other"]]]]})
        self.assertEqual(convert(text), "[my macos I](https://example.notion.site/other)\n")

    def test_bookmark_is_a_short_include_with_details_kept_as_data(self):
        bookmark = block(
            "b",
            "bookmark",
            properties={"link": [["https://reddit.com/r/x"]], "title": [['Say "hi"']]},
            format={"bookmark_icon": "https://icon"},
        )
        converter = converter_for(bookmark)
        self.assertEqual(converter.convert(PAGE), '{% include card.html url="https://reddit.com/r/x" %}\n')
        self.assertEqual(
            converter.previews, {"https://reddit.com/r/x": {"title": 'Say "hi"', "icon": "https://icon"}}
        )

    def test_bot_check_titles_fall_back_to_the_domain(self):
        bookmark = block(
            "b",
            "bookmark",
            properties={
                "link": [["https://www.site.com/q"]],
                "title": [["Just a moment..."]],
                "description": [["Checking your browser"]],
            },
        )
        converter = converter_for(bookmark)
        converter.convert(PAGE)
        self.assertEqual(converter.previews, {"https://www.site.com/q": {"title": "site.com"}})

    def test_github_link_preview_needs_no_preview_data(self):
        preview = block("e", "external_object_instance")
        converter = converter_for(
            preview, cache=LocalCache(link_urls={"e": "https://github.com/neovim/neovim"})
        )
        md = converter.convert(PAGE)
        self.assertEqual(md, '{% include card.html url="https://github.com/neovim/neovim" %}\n')
        self.assertEqual(converter.previews, {})

    def test_link_only_callout_is_a_tagged_quote_around_the_card(self):
        card = block("b", "bookmark", properties={"link": [["https://a.com"]]}, nested=True)
        md = convert(block("c", "callout", content=["b"], format={"page_icon": "📣"}), card)
        self.assertEqual(md, '> {% include card.html url="https://a.com" %}\n{: .callout .callout-link}\n')

    def test_text_callout_starts_with_its_emoji(self):
        md = convert(block("c", "callout", "note", format={"page_icon": "📣"}))
        self.assertEqual(md, "> 📣 note\n{: .callout}\n")

    def test_emoji_appears_once_when_callout_text_is_nested(self):
        child = block("t", "text", "shoutout", nested=True)
        md = convert(block("c", "callout", content=["t"], format={"page_icon": "📣"}), child)
        self.assertEqual(md, "> 📣 shoutout\n{: .callout}\n")

    def test_lists_inside_callouts_stay_tight(self):
        items = [block(f"i{n}", "bulleted_list", f"item {n}", nested=True) for n in (1, 2)]
        md = convert(block("c", "callout", "list", content=["i1", "i2"]), *items)
        self.assertEqual(md, "> list\n>\n> - item 1\n> - item 2\n{: .callout}\n")

    def test_multi_paragraph_callouts_stay_one_quote(self):
        child = block("t", "text", "second", nested=True)
        md = convert(block("c", "callout", "first", content=["t"]), child)
        self.assertEqual(md, "> first\n>\n> second\n{: .callout}\n")

    def test_code_blocks_keep_raw_text(self):
        code = block("k", "code", properties={"title": [["x = 1", [["b"]]]], "language": [["Python"]]})
        self.assertEqual(convert(code), "```python\nx = 1\n```\n")

    def test_toggle_summary_is_html(self):
        md = convert(block("g", "toggle", properties={"title": [["updates", [["b"]]]]}))
        self.assertTrue(md.startswith('<details markdown="1"><summary><strong>updates</strong></summary>'))


class NestedContentTest(unittest.TestCase):
    def test_quote_with_only_nested_paragraphs_keeps_them_inside(self):
        first = block("a", "text", "I thought so.", nested=True)
        second = block("b", "text", "Then I opened a PDF.", nested=True)
        md = convert(block("q", "quote", content=["a", "b"]), first, second)
        self.assertEqual(md, "> I thought so.\n>\n> Then I opened a PDF.\n")

    def test_empty_quote_is_dropped(self):
        self.assertEqual(convert(block("q", "quote", ""), block("t", "text", "after")), "after\n")

    def test_numbered_item_children_stay_inside_the_item(self):
        card = block("b", "bookmark", properties={"link": [["https://maps.app/x"]]}, nested=True)
        note = block("t", "text", "budget", nested=True)
        md = convert(block("n", "numbered_list", "Udon", content=["b", "t"]), card, note)
        self.assertEqual(md, '1. Udon\n\n   {% include card.html url="https://maps.app/x" %}\n\n   budget\n')


class TidyTest(unittest.TestCase):
    def test_lists_are_tight(self):
        self.assertEqual(tidy("- a\n\n- b\n\n  - c\n\ntext"), "- a\n- b\n  - c\n\ntext\n")

    def test_divider_under_heading_is_dropped(self):
        self.assertEqual(tidy("## Title\n\n---\n\ntext\n\n---"), "## Title\n\ntext\n\n---\n")

    def test_blank_runs_collapse(self):
        self.assertEqual(tidy("a\n\n\n\nb"), "a\n\nb\n")


class RewritePostLinksTest(unittest.TestCase):
    TARGETS = {
        "30ef432196de80b287f2e297420d1d46": "/blog/macos-setup-i/",
        "shell-tools": "/blog/shell-toolkit-i/",
    }

    def rewrite(self, markdown: str) -> str:
        return rewrite_post_links(markdown, "nodokas.notion.site", self.TARGETS)

    def test_page_id_links_become_post_urls(self):
        md = "[my macos I](https://nodokas.notion.site/30ef432196de80b287f2e297420d1d46)"
        self.assertEqual(self.rewrite(md), "[my macos I](/blog/macos-setup-i/)")

    def test_readable_title_urls_with_query_strings_match_by_id(self):
        md = "(https://nodokas.notion.site/macOS-Optimization-30ef432196de80b287f2e297420d1d46?source=copy_link)"
        self.assertEqual(self.rewrite(md), "(/blog/macos-setup-i/)")

    def test_custom_slugs_match(self):
        md = "[NEW PAGE](https://nodokas.notion.site/shell-tools?source=copy_link)"
        self.assertEqual(self.rewrite(md), "[NEW PAGE](/blog/shell-toolkit-i/)")

    def test_other_notion_pages_are_left_alone(self):
        md = "[x](https://nodokas.notion.site/unrelated-page)"
        self.assertEqual(self.rewrite(md), md)


class LiquidStrTest(unittest.TestCase):
    def test_escapes_quotes_and_braces(self):
        self.assertEqual(liquid_str(' {{ "x" }} '), "&#123;&#123; &quot;x&quot; &#125;&#125;")


if __name__ == "__main__":
    unittest.main()
