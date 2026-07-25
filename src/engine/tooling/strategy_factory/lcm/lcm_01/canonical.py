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


def digest_object(value: Any, digest_field: str | None = None) -> str:
    if digest_field and isinstance(value, dict):
        value = {key: item for key, item in value.items() if key != digest_field}
    return sha256_bytes(canonical_json_bytes(value))


def content_id(prefix: str, material: Any, length: int = 32) -> str:
    digest = hashlib.sha256(canonical_json_bytes(material)).hexdigest()
    return f"{prefix}_{digest[:length].upper()}"


def normalize_root_relative(raw: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ContractViolation("path must be non-empty")
    normalized_raw = raw.replace("\\", "/")
    path = PurePosixPath(normalized_raw)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ContractViolation(f"unsafe path: {raw}")
    return path.as_posix()


def stable_text_digest(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(normalized.encode("utf-8"))
