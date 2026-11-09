"""Download a post's images into the repo so posts don't depend on Notion or expiring links."""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

from .notion_api import TIMEOUT_S, USER_AGENT

log = logging.getLogger(__name__)

MAX_WIDTH_PX = 1440  # 2x the 720px post column
MAX_COVER_WIDTH_PX = 720  # card thumbnails show at about a third of the column
EXTENSIONS = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}
MARKDOWN_IMAGE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\))")


def localize_images(markdown: str, site_domain: str, asset_dir: Path, public_prefix: str) -> str:
    """Download images served by the Notion site into asset_dir and point the Markdown at them.

    Images hosted elsewhere are left as-is. public_prefix is the URL path for asset_dir,
    e.g. "/assets/blog/my-post".
    """
    notion_prefix = f"https://{site_domain}/image/"
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        url = match.group(2)
        if not url.startswith(notion_prefix):
            return match.group(0)
        count += 1
        filename = _download(url, asset_dir, f"{count}")
        return f"{match.group(1)}{public_prefix}/{filename}{match.group(3)}"

    return MARKDOWN_IMAGE.sub(replace, markdown)


def localize_preview_images(
    previews: dict[str, dict[str, str]], asset_dir: Path, public_prefix: str
) -> dict[str, dict[str, str]]:
    """Save link-card thumbnails locally; drop ones that no longer load (e.g. expired Maps photos)."""
    localized = {}
    for number, (url, preview) in enumerate(previews.items(), start=1):
        image = preview.get("image")
        if not image or image.startswith("/"):
            localized[url] = preview
            continue
        rest = {key: value for key, value in preview.items() if key != "image"}
        try:
            filename = _download(image, asset_dir, f"cover-{number}", MAX_COVER_WIDTH_PX)
        except (OSError, ValueError) as err:
            log.info("dropping card thumbnail that no longer loads: %s (%s)", image[:80], err)
            localized[url] = rest
            continue
        localized[url] = {**rest, "image": f"{public_prefix}/{filename}"}
    return localized


def _download(url: str, asset_dir: Path, stem: str, max_width: int = MAX_WIDTH_PX) -> str:
    request = urllib.request.Request(url, headers={"user-agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
        content_type = response.headers.get_content_type()
        if content_type not in EXTENSIONS:
            raise ValueError(f"{url} returned {content_type}, not an image")
        data = response.read()
    asset_dir.mkdir(parents=True, exist_ok=True)
    path = asset_dir / f"{stem}{EXTENSIONS[content_type]}"
    path.write_bytes(data)
    _shrink(path, max_width)
    log.info("saved %s (%d KB)", path, path.stat().st_size // 1024)
    return path.name


def _shrink(path: Path, max_width: int) -> None:
    """Cap the width using macOS `sips` when available; otherwise keep the original."""
    if shutil.which("sips") is None:
        log.warning("sips not found; %s kept at full size", path)
        return
    if _width(path) <= max_width:
        return
    subprocess.run(["sips", "--resampleWidth", str(max_width), str(path)], check=True, capture_output=True)


def _width(path: Path) -> int:
    result = subprocess.run(
        ["sips", "--getProperty", "pixelWidth", str(path)], check=True, capture_output=True, text=True
    )
    return int(result.stdout.rsplit(":", 1)[-1].strip())
