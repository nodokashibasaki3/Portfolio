"""Read public Notion pages through the unofficial v3 API that notion.site pages use."""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger(__name__)

Block = dict[str, Any]

USER_AGENT = "Mozilla/5.0"  # Notion rejects Python's default user agent with 403.
TIMEOUT_S = 30
MAX_ATTEMPTS = 3
RETRY_DELAY_S = 2
CHUNK_LIMIT = 100
MAX_CHUNKS = 50
MAX_FILL_ROUNDS = 10
UPLOADED_PREFIXES = ("attachment:",)
UPLOADED_HOSTS = ("secure.notion-static", "prod-files-secure")


def unwrap(record: dict[str, Any]) -> Block:
    """Records come back as {"value": block} or {"value": {"value": block, "role": ...}}."""
    value = record.get("value", {})
    if "type" not in value and "value" in value:
        return value["value"]
    return value


class NotionClient:
    """Fetches page blocks and page titles from a public Notion site."""

    def __init__(self, site_domain: str, space_id: str) -> None:
        self.site_domain = site_domain
        self.space_id = space_id
        self._api = f"https://{site_domain}/api/v3/"
        self._titles: dict[str, str | None] = {}

    def page_url(self, page_id: str) -> str:
        return f"https://{self.site_domain}/{page_id.replace('-', '')}"

    def image_url(self, block: Block) -> str:
        """Public URL for an image block; uploaded files go through the site's image proxy."""
        source = "".join(seg[0] for seg in block.get("properties", {}).get("source") or [])
        if not source.startswith(UPLOADED_PREFIXES) and not any(host in source for host in UPLOADED_HOSTS):
            return source
        quoted = urllib.parse.quote(source, safe="")
        return f"https://{self.site_domain}/image/{quoted}?table=block&id={block['id']}"

    def load_page(self, page_id: str) -> dict[str, Block]:
        """Return {block_id: block} for every block on the page, including nested ones."""
        blocks: dict[str, Block] = {}
        cursor: dict[str, Any] = {"stack": []}
        for chunk in range(MAX_CHUNKS):
            data = self._post(
                "loadCachedPageChunkV2",
                {
                    "page": {"id": page_id},
                    "limit": CHUNK_LIMIT,
                    "cursor": cursor,
                    "chunkNumber": chunk,
                    "verticalColumns": False,
                },
            )
            blocks.update(self._blocks_in(data))
            cursors = data.get("cursors") or []
            if not cursors:
                break
            cursor = cursors[0] if isinstance(cursors[0], dict) else {"stack": cursors[0]}
        return {**blocks, **self._fetch_missing_children(blocks)}

    def page_title(self, page_id: str) -> str | None:
        """Title of another page (for page links), or None if it isn't public."""
        if page_id not in self._titles:
            self._titles[page_id] = self._lookup_title(page_id)
        return self._titles[page_id]

    def _lookup_title(self, page_id: str) -> str | None:
        try:
            data = self._sync([page_id], with_space=True)
        except OSError as err:
            log.warning("title lookup for page %s failed: %s", page_id, err)
            return None
        block = self._blocks_in(data).get(page_id, {})
        title = block.get("properties", {}).get("title", [])
        return "".join(segment[0] for segment in title) or None

    def _fetch_missing_children(self, blocks: dict[str, Block]) -> dict[str, Block]:
        """Large pages omit some nested blocks from the chunk responses; fetch them directly."""
        found: dict[str, Block] = {}
        for _ in range(MAX_FILL_ROUNDS):
            known = {**blocks, **found}
            missing = {
                child
                for block in known.values()
                for child in block.get("content") or []
                if child not in known
            }
            if not missing:
                break
            fetched = self._blocks_in(self._sync(sorted(missing)))
            if not fetched:
                log.warning("%d nested blocks are not public", len(missing))
                break
            found.update(fetched)
        return found

    def _sync(self, block_ids: list[str], with_space: bool = False) -> dict[str, Any]:
        def pointer(block_id: str) -> dict[str, str]:
            ptr = {"table": "block", "id": block_id}
            return {**ptr, "spaceId": self.space_id} if with_space else ptr

        requests = [{"pointer": pointer(i), "version": -1} for i in block_ids]
        return self._post("syncRecordValuesMain", {"requests": requests})

    @staticmethod
    def _blocks_in(data: dict[str, Any]) -> dict[str, Block]:
        records = data.get("recordMap", {}).get("block", {})
        return {block_id: unwrap(record) for block_id, record in records.items()}

    def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            self._api + endpoint,
            data=json.dumps(payload).encode(),
            headers={"content-type": "application/json", "user-agent": USER_AGENT},
        )
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
                    return json.load(response)
            except urllib.error.HTTPError:
                raise  # the server answered; retrying won't change a 4xx/5xx here
            except OSError as err:  # connection resets and timeouts are usually transient
                if attempt == MAX_ATTEMPTS:
                    raise
                log.info("%s failed (%s); retrying", endpoint, err)
                time.sleep(RETRY_DELAY_S * attempt)
        raise AssertionError("unreachable")
