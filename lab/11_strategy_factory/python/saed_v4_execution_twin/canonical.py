from __future__ import annotations
import hashlib
import json
import math
from typing import Any


def _normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _normalize(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalize(v) for v in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite float is not canonical")
        if value == 0.0:
            return 0.0
        return float(format(value, ".15g"))
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}_{content_hash(value)[:24]}"


def deterministic_unit_interval(*parts: str) -> float:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    integer = int.from_bytes(digest[:8], "big")
    return integer / float(2**64 - 1)


def merkle_root(hashes: list[str]) -> str:
    if not hashes:
        return hashlib.sha256(b"").hexdigest()
    layer = [bytes.fromhex(h) for h in hashes]
    while len(layer) > 1:
        if len(layer) % 2:
            layer.append(layer[-1])
        layer = [hashlib.sha256(layer[i] + layer[i + 1]).digest() for i in range(0, len(layer), 2)]
    return layer[0].hex()
