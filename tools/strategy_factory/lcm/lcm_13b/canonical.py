from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest_object(value: Any, digest_field: str | None = None) -> str:
    if digest_field and isinstance(value, dict):
        value = {k: v for k, v in value.items() if k != digest_field}
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def stable_id(prefix: str, *parts: object, length: int = 32) -> str:
    raw = "|".join(str(x) for x in parts)
    return f"{prefix}_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:length].upper()}"

def verify_embedded_digest(value: dict[str, Any], field: str) -> bool:
    return isinstance(value.get(field), str) and value[field] == digest_object(value, field)
