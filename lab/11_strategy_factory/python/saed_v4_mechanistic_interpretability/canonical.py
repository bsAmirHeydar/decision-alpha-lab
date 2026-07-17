from __future__ import annotations
import hashlib
import json
from typing import Any

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}_{content_hash(value)[:24]}"

def with_identity(prefix: str, value: dict[str, Any], id_field: str, hash_field: str) -> dict[str, Any]:
    payload = dict(value)
    payload[id_field] = stable_id(prefix, value)
    payload[hash_field] = content_hash(payload)
    return payload
