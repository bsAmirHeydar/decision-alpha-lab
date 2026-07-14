"""Canonical serialization, hashing, and time helpers."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def content_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def file_hash(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return dt.astimezone(timezone.utc)


def stable_id(prefix: str, payload: Any, length: int = 24) -> str:
    return f"{prefix}_{content_hash(payload)[:length]}"


def hash_paths(root: str | Path, paths: Iterable[str]) -> dict[str, str]:
    root_path = Path(root)
    result: dict[str, str] = {}
    for rel in sorted(set(paths)):
        p = root_path / rel
        if not p.is_file():
            raise FileNotFoundError(rel)
        result[rel.replace("\\", "/")] = file_hash(p)
    return result
