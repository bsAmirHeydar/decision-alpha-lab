from __future__ import annotations
import hashlib
import json
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_object(value: Any, digest_field: str | None = None) -> str:
    if digest_field and isinstance(value, dict):
        value = {k: v for k, v in value.items() if k != digest_field}
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def content_id(prefix: str, value: Any, width: int = 32) -> str:
    return prefix + "_" + hashlib.sha256(canonical_bytes(value)).hexdigest()[:width].upper()


def file_digest(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()
