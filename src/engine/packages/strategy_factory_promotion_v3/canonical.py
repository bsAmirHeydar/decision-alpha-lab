"""Canonical JSON and identity primitives shared by every I12 artifact."""
from __future__ import annotations
import hashlib, json, math
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any
from .errors import PromotionError

def canonical_value(value: Any) -> Any:
    if is_dataclass(value): return canonical_value(asdict(value))
    if isinstance(value, Enum): return value.value
    if isinstance(value, Path): return value.as_posix()
    if isinstance(value, dict): return {str(k): canonical_value(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)): return [canonical_value(v) for v in value]
    if isinstance(value, float):
        if not math.isfinite(value): raise PromotionError("non_finite_canonical_value", "NaN and Infinity are forbidden")
        return 0.0 if value == 0.0 else float(format(value, ".15g"))
    if value is None or isinstance(value, (str, int, bool)): return value
    raise PromotionError("unsupported_canonical_type", "unsupported canonical type", {"type": type(value).__name__})

def canonical_json(value: Any) -> str:
    return json.dumps(canonical_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def stable_id(prefix: str, value: Any, length: int = 24) -> str:
    if not prefix or not prefix.replace("_", "").isalnum(): raise PromotionError("invalid_id_prefix", "invalid stable-id prefix")
    if not 8 <= length <= 64: raise PromotionError("invalid_id_length", "digest length must be 8..64")
    return f"{prefix}_{canonical_sha256(value)[:length]}"
