from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

FNV1A_64_OFFSET = 14695981039346656037
FNV1A_64_PRIME = 1099511628211
MASK64 = (1 << 64) - 1

def fnv1a64_utf16le(value: str) -> int:
    result = FNV1A_64_OFFSET
    for byte in value.encode("utf-16le"):
        result ^= byte
        result = (result * FNV1A_64_PRIME) & MASK64
    return result

def stable_id(prefix: str, payload: str) -> str:
    return f"{prefix}_{fnv1a64_utf16le(payload):016x}"

def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        return _normalize(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in sorted(value.items(), key=lambda x: str(x[0]))}
    if isinstance(value, (tuple, list)):
        return [_normalize(v) for v in value]
    return value

def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def canonical_hash(value: Any, prefix: str = "hash") -> str:
    return stable_id(prefix, canonical_json(value))
