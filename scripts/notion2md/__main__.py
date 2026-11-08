"""Export the Notion blog posts to Markdown drafts for this Jekyll site.

Usage (from the repo root):
    python3 -m scripts.notion2md --out /tmp/notion-drafts
    python3 -m scripts.notion2md --out /tmp/notion-drafts --only macos-setup-ii

Each draft gets `layout: post` and a title; add the date (via the `_posts/YYYY-MM-DD-slug.md`
filename) when moving it into `_posts/`. GitHub link previews and people's names come from the
Notion desktop app's local cache when it is installed; otherwise they show as [link?]/[person?].
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from .convert import Converter
from .local_cache import DEFAULT_DB, load_local_cache
from .notion_api import NotionClient

SITE_DOMAIN = "nodokas.notion.site"
SPACE_ID = "8b1e0495-2533-4ff8-95f6-6f4e1e043a81"


@dataclass(frozen=True)
class Post:
    slug: str
    page_id: str
    title: str  # matches _data/blog.yml


POSTS = (
    Post("macos-setup-ii", "314f4321-96de-808e-8377-da577a5c4c3a", "Introducing my macOS Setup II"),
    Post("shell-toolkit-i", "314f4321-96de-8026-a052-f8f27fa643bf", "Introducing my Shell Toolkit I"),
    Post(
        "qwen-agentic-coding", "324f4321-96de-80ae-92d3-cb7644db914c", "Setting up Qwen for Agentic Coding!"
    ),
    Post("raycast-toolkit", "312f4321-96de-8013-a2a7-e2e25b6e8164", "Introducing my Raycast Toolkit"),
    Post("macos-setup-i", "30ef4321-96de-80b2-87f2-e297420d1d46", "Introducing my macOS Setup I"),
    Post("open-source-contribution-i", "310f4321-96de-808e-92f9-f657c94c6f0d", "Open Source Contribution I"),
    Post("tokyo-food-review", "2d3f4321-96de-817b-8033-f41e42cf33ac", "Tokyo Food Review"),
)


def front_matter(title: str) -> str:
    escaped = title.replace('"', '\\"')
    return f'---\nlayout: post\ntitle: "{escaped}"\n---\n\n'


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python3 -m scripts.notion2md", description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, required=True, help="directory to write <slug>.md drafts into")
    parser.add_argument("--only", nargs="+", choices=[p.slug for p in POSTS], help="export only these posts")
    parser.add_argument("--notion-db", type=Path, default=DEFAULT_DB, help="Notion desktop app cache")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    client = NotionClient(SITE_DOMAIN, SPACE_ID)
    cache = load_local_cache(args.notion_db)
    if not cache.link_urls:
        logging.warning("Notion app cache not found at %s; link previews will be missing", args.notion_db)

    args.out.mkdir(parents=True, exist_ok=True)
    posts = [p for p in POSTS if not args.only or p.slug in args.only]
    failures = 0
    for post in posts:
        try:
            blocks = client.load_page(post.page_id)
            body = Converter(blocks, cache, client).convert(post.page_id)
        except OSError as err:  # network errors: report and keep exporting the other posts
            logging.error("%s: could not fetch from Notion: %s", post.slug, err)
            failures += 1
            continue
        path = args.out / f"{post.slug}.md"
        path.write_text(front_matter(post.title) + body)
        logging.info("%s: %d blocks -> %s", post.slug, len(blocks), path)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
