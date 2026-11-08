"""Unit tests for the Notion -> Markdown conversion (no network).

Run from the repo root: python3 -m unittest scripts.notion2md.test_convert
"""

from __future__ import annotations

import unittest
from typing import Any

from .convert import Converter, liquid_str, tidy
from .local_cache import LocalCache
from .rich_text import first_url, plain_text, to_html, to_markdown

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


def convert(*children: dict, cache: LocalCache | None = None) -> str:
    blocks = {child["id"]: child for child in children}
    top_level = [c["id"] for c in children if not c.get("nested")]
    blocks[PAGE] = block(PAGE, "page", "Post", top_level)
    return Converter(blocks, cache or LocalCache(), FakePages()).convert(PAGE)


class RichTextTest(unittest.TestCase):
    def test_marks_render_as_markdown(self):
        segments = [["bold", [["b"]]], [" and "], ["code", [["c"]]], [" "], ["link", [["a", "https://x.y"]]]]
        self.assertEqual(to_markdown(segments, str), "**bold** and `code` [link](https://x.y)")

    def test_mentions_use_the_mention_renderer(self):
        segments = [["‣", [["u", "user-1"]]]]
        self.assertEqual(to_markdown(segments, lambda mark: f"<{mark[1]}>"), "<user-1>")

    def test_html_escapes_text(self):
        self.assertEqual(to_html([["a < b", [["b"]]]]), "<strong>a &lt; b</strong>")

    def test_first_url_prefers_order_in_text(self):
        segments = [["x"], ["‣", [["eoi", "e1"]]], ["y", [["a", "https://later"]]]]
        self.assertEqual(first_url(segments, {"e1": "https://github.com/a/b"}), "https://github.com/a/b")

    def test_plain_text_ignores_marks(self):
        self.assertEqual(plain_text([["a", [["b"]]], ["b"]]), "ab")


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

    def test_bookmark_becomes_a_card_include(self):
        bookmark = block(
            "b",
            "bookmark",
            properties={"link": [["https://reddit.com/r/x"]], "title": [['Say "hi"']]},
            format={"bookmark_icon": "https://icon"},
        )
        self.assertEqual(
            convert(bookmark),
            '{% include bookmark.html url="https://reddit.com/r/x" title="Say &quot;hi&quot;" '
            'icon="https://icon" %}\n',
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
        self.assertEqual(
            convert(bookmark), '{% include bookmark.html url="https://www.site.com/q" title="site.com" %}\n'
        )

    def test_github_link_preview_becomes_a_github_card(self):
        preview = block("e", "external_object_instance")
        md = convert(preview, cache=LocalCache(link_urls={"e": "https://github.com/neovim/neovim"}))
        self.assertEqual(md, '{% include github-card.html url="https://github.com/neovim/neovim" %}\n')

    def test_link_only_callout_holds_just_the_card(self):
        card = block("b", "bookmark", properties={"link": [["https://a.com"]]}, nested=True)
        md = convert(block("c", "callout", content=["b"]), card)
        self.assertIn('<div class="callout callout-link">', md)
        self.assertNotIn("callout-icon", md)

    def test_text_callout_uses_its_emoji(self):
        md = convert(block("c", "callout", "note", format={"page_icon": "📣"}))
        self.assertIn('<span class="callout-icon" aria-hidden="true">📣</span>', md)

    def test_text_callout_without_emoji_uses_the_link_favicon(self):
        text = block(
            "c", "callout", properties={"title": [["see ", []], ["here", [["a", "https://raycast.com/x"]]]]}
        )
        self.assertIn("favicons?domain=raycast.com", convert(text))

    def test_code_blocks_keep_raw_text(self):
        code = block("k", "code", properties={"title": [["x = 1", [["b"]]]], "language": [["Python"]]})
        self.assertEqual(convert(code), "```python\nx = 1\n```\n")

    def test_toggle_summary_is_html(self):
        md = convert(block("g", "toggle", properties={"title": [["updates", [["b"]]]]}))
        self.assertTrue(md.startswith('<details markdown="1"><summary><strong>updates</strong></summary>'))


class TidyTest(unittest.TestCase):
    def test_lists_are_tight(self):
        self.assertEqual(tidy("- a\n\n- b\n\n  - c\n\ntext"), "- a\n- b\n  - c\n\ntext\n")

    def test_divider_under_heading_is_dropped(self):
        self.assertEqual(tidy("## Title\n\n---\n\ntext\n\n---"), "## Title\n\ntext\n\n---\n")

    def test_blank_runs_collapse(self):
        self.assertEqual(tidy("a\n\n\n\nb"), "a\n\nb\n")


class LiquidStrTest(unittest.TestCase):
    def test_escapes_quotes_and_braces(self):
        self.assertEqual(liquid_str(' {{ "x" }} '), "&#123;&#123; &quot;x&quot; &#125;&#125;")


if __name__ == "__main__":
    unittest.main()
