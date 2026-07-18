from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import ContractViolation


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def content_id(prefix: str, material: Any, length: int = 32) -> str:
    return f"{prefix}_{hashlib.sha256(canonical_json_bytes(material)).hexdigest()[:length].upper()}"


def digest_object(value: Any, digest_field: str | None = None) -> str:
    if digest_field and isinstance(value, dict):
        value = {k: v for k, v in value.items() if k != digest_field}
    return sha256_bytes(canonical_json_bytes(value))


def normalize_root_relative(raw: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ContractViolation("path must be a non-empty string")
    if "\\" in raw:
        raw = raw.replace("\\", "/")
    raw_parts = raw.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise ContractViolation(f"unsafe path forbidden: {raw}")
    p = PurePosixPath(raw)
    if p.is_absolute() or raw.startswith("/"):
        raise ContractViolation(f"absolute path forbidden: {raw}")
    if any(part in {"", ".", ".."} for part in p.parts):
        raise ContractViolation(f"unsafe path forbidden: {raw}")
    normalized = p.as_posix()
    if normalized.startswith("../") or "/../" in normalized:
        raise ContractViolation(f"path traversal forbidden: {raw}")
    return normalized
