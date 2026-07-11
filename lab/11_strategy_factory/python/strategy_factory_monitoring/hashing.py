from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

FNV_OFFSET=14695981039346656037
FNV_PRIME=1099511628211
MASK=(1<<64)-1

def fnv1a_utf16le(value: str) -> int:
    h=FNV_OFFSET
    for b in value.encode("utf-16le"):
        h ^= b
        h = (h * FNV_PRIME) & MASK
    return h

def stable_id(*parts: object) -> str:
    return f"{fnv1a_utf16le('|'.join(str(x) for x in parts)):016x}"

def _normalise(value: Any) -> Any:
    if is_dataclass(value):
        return {k:_normalise(v) for k,v in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k):_normalise(v) for k,v in sorted(value.items(), key=lambda kv:str(kv[0]))}
    if isinstance(value, (list,tuple)):
        return [_normalise(v) for v in value]
    return value

def canonical_json(value: Any) -> str:
    return json.dumps(_normalise(value), sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False)

def canonical_hash(value: Any) -> str:
    return stable_id(canonical_json(value))
