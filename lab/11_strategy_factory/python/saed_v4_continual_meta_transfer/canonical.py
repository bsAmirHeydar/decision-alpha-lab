from __future__ import annotations

import hashlib
import json
import math
from typing import Any


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite float")
        return float(format(value, ".15g"))
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        _normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def stable_id(prefix: str, value: Any, length: int = 24) -> str:
    if not prefix or not prefix.replace("_", "").isalnum():
        raise ValueError("invalid stable-id prefix")
    if length < 12 or length > 64:
        raise ValueError("stable-id digest length outside policy")
    return f"{prefix}_{content_hash(value)[:length]}"


def seal(value: dict[str, Any], field: str = "artifact_hash") -> dict[str, Any]:
    output = dict(value)
    output[field] = content_hash({key: item for key, item in output.items() if key != field})
    return output
