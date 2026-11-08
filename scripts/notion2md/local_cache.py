"""Read data the public API hides from the Notion desktop app's local cache.

The public API returns link previews (e.g. GitHub mentions) and people mentions without their
URLs or names, but the desktop app caches both in a SQLite database. We read a temporary copy
so the running app's database is never locked or modified.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import tempfile
from contextlib import closing
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_DB = Path.home() / "Library/Application Support/Notion/notion.db"
SQLITE_SIDECARS = ("-wal", "-shm")


@dataclass(frozen=True)
class LocalCache:
    link_urls: dict[str, str] = field(default_factory=dict)  # external object id -> URL
    user_names: dict[str, str] = field(default_factory=dict)  # user id -> display name


def load_local_cache(db_path: Path = DEFAULT_DB) -> LocalCache:
    """Load link URLs and user names, or an empty cache if the desktop app isn't installed."""
    db_path = Path(db_path)
    if not db_path.exists():
        return LocalCache()
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / db_path.name
        shutil.copy2(db_path, copy)
        for suffix in SQLITE_SIDECARS:
            sidecar = db_path.with_name(db_path.name + suffix)
            if sidecar.exists():
                shutil.copy2(sidecar, copy.with_name(copy.name + suffix))
        with closing(sqlite3.connect(f"file:{copy}?mode=ro", uri=True)) as con:
            return LocalCache(link_urls=_link_urls(con), user_names=_user_names(con))


def _link_urls(con: sqlite3.Connection) -> dict[str, str]:
    rows = con.execute("select id, format from block where type = 'external_object_instance'")
    urls = {}
    for block_id, fmt in rows:
        url = json.loads(fmt).get("original_url") if fmt else None
        if url:
            urls[block_id] = url
    return urls


def _user_names(con: sqlite3.Connection) -> dict[str, str]:
    rows = con.execute("select id, name from notion_user where name is not null")
    return dict(rows.fetchall())
