"""Export the Notion blog posts into this Jekyll site.

Usage (from the repo root):
    python3 -m scripts.notion2md                       # all posts -> _posts/, images -> assets/blog/
    python3 -m scripts.notion2md --only macos-setup-ii
    python3 -m scripts.notion2md --out /tmp/drafts     # preview elsewhere

Writes `_posts/YYYY-MM-DD-slug.md` with front matter, downloads Notion-hosted images into
`assets/blog/<slug>/`, and points links between exported posts at their pages on this site.
GitHub link previews and people's names come from the Notion desktop app's local cache when it
is installed; otherwise they show as [link?]/[person?].
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from .convert import Converter
from .images import localize_card_covers, localize_images
from .links import rewrite_post_links
from .local_cache import DEFAULT_DB, LocalCache, load_local_cache
from .notion_api import NotionClient

SITE_DOMAIN = "nodokas.notion.site"
SPACE_ID = "8b1e0495-2533-4ff8-95f6-6f4e1e043a81"
ASSET_URL_PREFIX = "/assets/blog"


@dataclass(frozen=True)
class Post:
    slug: str
    date: str  # YYYY-MM-DD publish date
    page_id: str
    title: str  # matches _data/blog.yml
    notion_slug: str | None = None  # custom nodokas.notion.site/<slug> URL, if any

    @property
    def name(self) -> str:
        """Jekyll post name, as used by `{% post_url %}` and the _posts filename."""
        return f"{self.date}-{self.slug}"


POSTS = (
    Post(
        "macos-setup-ii",
        "2026-05-31",
        "314f4321-96de-808e-8377-da577a5c4c3a",
        "Introducing my macOS Setup II",
    ),
    Post(
        "shell-toolkit-i",
        "2026-04-29",
        "314f4321-96de-8026-a052-f8f27fa643bf",
        "Introducing my Shell Toolkit I",
        notion_slug="shell-tools",
    ),
    Post(
        "qwen-agentic-coding",
        "2026-03-15",
        "324f4321-96de-80ae-92d3-cb7644db914c",
        "Setting up Qwen for Agentic Coding!",
        notion_slug="running-local-model",
    ),
    Post(
        "raycast-toolkit",
        "2026-03-10",
        "312f4321-96de-8013-a2a7-e2e25b6e8164",
        "Introducing my Raycast Toolkit",
        notion_slug="raycast-toolkit",
    ),
    Post(
        "macos-setup-i", "2026-02-21", "30ef4321-96de-80b2-87f2-e297420d1d46", "Introducing my macOS Setup I"
    ),
    Post(
        "open-source-contribution-i",
        "2026-02-22",
        "310f4321-96de-808e-92f9-f657c94c6f0d",
        "Open Source Contribution I",
    ),
    Post("tokyo-food-review", "2026-01-01", "2d3f4321-96de-817b-8033-f41e42cf33ac", "Tokyo Food Review"),
)


def link_targets(posts: tuple[Post, ...]) -> dict[str, str]:
    """Notion page ids and custom slugs -> Jekyll post names, for cross-post links."""
    targets = {post.page_id.replace("-", ""): post.name for post in posts}
    targets.update({post.notion_slug: post.name for post in posts if post.notion_slug})
    return targets


def front_matter(title: str) -> str:
    escaped = title.replace('"', '\\"')
    return f'---\nlayout: post\ntitle: "{escaped}"\n---\n\n'


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python3 -m scripts.notion2md", description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, default=Path("_posts"), help="where to write posts")
    parser.add_argument("--assets", type=Path, default=Path("assets/blog"), help="where to save images")
    parser.add_argument("--only", nargs="+", choices=[p.slug for p in POSTS], help="export only these posts")
    parser.add_argument("--notion-db", type=Path, default=DEFAULT_DB, help="Notion desktop app cache")
    return parser.parse_args(argv)


def export(post: Post, client: NotionClient, cache: LocalCache, args: argparse.Namespace) -> Path:
    blocks = client.load_page(post.page_id)
    body = Converter(blocks, cache, client).convert(post.page_id)
    body = rewrite_post_links(body, SITE_DOMAIN, link_targets(POSTS))
    asset_dir, asset_url = args.assets / post.slug, f"{ASSET_URL_PREFIX}/{post.slug}"
    body = localize_images(body, SITE_DOMAIN, asset_dir, asset_url)
    body = localize_card_covers(body, asset_dir, asset_url)
    path = args.out / f"{post.name}.md"
    path.write_text(front_matter(post.title) + body)
    logging.info("%s: %d blocks -> %s", post.slug, len(blocks), path)
    return path


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = parse_args(argv)
    client = NotionClient(SITE_DOMAIN, SPACE_ID)
    cache = load_local_cache(args.notion_db)
    if not cache.link_urls:
        logging.warning("Notion app cache not found at %s; link previews will be missing", args.notion_db)

    args.out.mkdir(parents=True, exist_ok=True)
    failures = 0
    for post in (p for p in POSTS if not args.only or p.slug in args.only):
        try:
            export(post, client, cache, args)
        except (OSError, ValueError) as err:  # network or bad image: keep exporting the others
            logging.error("%s: export failed: %s", post.slug, err)
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
