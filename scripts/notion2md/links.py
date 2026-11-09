"""Point links to other exported Notion posts at their pages on this site."""

from __future__ import annotations

import re

HEX_ID = re.compile(r"[0-9a-f]{32}$")


def rewrite_post_links(markdown: str, site_domain: str, targets: dict[str, str]) -> str:
    """Replace links to exported Notion pages with Jekyll `{% post_url %}` tags.

    targets maps a page key to a post name (`YYYY-MM-DD-slug`). A key is either a page id
    without dashes or a custom notion.site slug (e.g. "shell-tools"). Notion URLs may also be
    "Readable-Title-<id>" and carry query strings like ?source=copy_link.
    """
    pattern = re.compile(rf"https://{re.escape(site_domain)}/([A-Za-z0-9-]+)(?:\?[^)\s\"]*)?")

    def replace(match: re.Match[str]) -> str:
        path = match.group(1)
        page_id = HEX_ID.search(path.replace("-", "").lower())
        key = page_id.group(0) if page_id and page_id.group(0) in targets else path
        post = targets.get(key)
        return f"{{% post_url {post} %}}" if post else match.group(0)

    return pattern.sub(replace, markdown)
