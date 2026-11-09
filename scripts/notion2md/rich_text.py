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
    for segment in _merge_same_marks(segments or []):
        text, marks = segment[0], _marks(segment)
        if text == MENTION_CHAR and marks:
            out.append(mention(marks[0]))
        else:
            out.append(_apply_marks(text, marks))
    return "".join(out)


def escape_pipes(text: str) -> str:
    """A literal | would make kramdown treat the line as a table row."""
    return text.replace("|", "\\|")


def _merge_same_marks(segments: list[Segment]) -> list[Segment]:
    """Join neighbors with identical formatting, so "**a****b**" renders as "**ab**"."""
    merged: list[Segment] = []
    for segment in segments:
        is_mention = segment[0] == MENTION_CHAR
        previous = merged[-1] if merged else None
        if (
            previous
            and not is_mention
            and previous[0] != MENTION_CHAR
            and _marks(previous) == _marks(segment)
        ):
            merged[-1] = [previous[0] + segment[0], *previous[1:]]
        else:
            merged.append(list(segment))
    return merged


def _apply_marks(text: str, marks: list[Mark]) -> str:
    is_code = any(mark[0] == "c" for mark in marks)
    if not is_code:
        text = escape_pipes(text)
    # Markdown emphasis can't start or end with a space ("**a **" stays literal),
    # so wrap only the inner text and keep surrounding whitespace outside the marks.
    core = text.strip()
    if not core:
        return text
    lead, trail = text[: len(text) - len(text.lstrip())], text[len(text.rstrip()) :]
    # Code goes innermost: "**`x`**" is bold code, while "`**x**`" shows the asterisks.
    for mark in sorted(marks, key=lambda m: m[0] != "c"):
        if mark[0] in MARKDOWN_MARKS:
            core = MARKDOWN_MARKS[mark[0]].format(core)
        elif mark[0] == "a":
            core = f"[{core}]({mark[1]})"
    return f"{lead}{core}{trail}"


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
