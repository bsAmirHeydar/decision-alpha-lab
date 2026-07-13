"""Canonical serialization primitives for UCE-I10 artifacts.

Canonical JSON is the identity substrate for every model state, view artifact,
qualification report, and registry snapshot. Non-finite values are rejected;
allowing NaN/Infinity would make hashes language- and parser-dependent.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any

from .errors import DeepViewError


def canonical_value(value: Any) -> Any:
    """Convert a value into the closed canonical JSON domain."""

    if is_dataclass(value):
        return canonical_value(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {
            str(key): canonical_value(value[key])
            for key in sorted(value, key=str)
        }
    if isinstance(value, (tuple, list)):
        return [canonical_value(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DeepViewError(
                "non_finite_canonical_value",
                "canonical artifacts cannot contain NaN or Infinity",
                {"value": repr(value)},
            )
        if value == 0.0:
            return 0.0
        return float(format(value, ".15g"))
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise DeepViewError(
        "unsupported_canonical_type",
        "value cannot be represented in canonical JSON",
        {"type": type(value).__name__},
    )


def canonical_json(value: Any) -> str:
    """Serialize a value with stable ordering and no insignificant spaces."""

    return json.dumps(
        canonical_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any, length: int = 24) -> str:
    if not prefix or not prefix.replace("_", "").isalnum():
        raise DeepViewError(
            "invalid_stable_id_prefix",
            "stable-id prefix must be non-empty and alphanumeric/underscore",
            {"prefix": prefix},
        )
    if length < 8 or length > 64:
        raise DeepViewError(
            "invalid_stable_id_length",
            "stable-id digest length must be between 8 and 64",
            {"length": length},
        )
    return f"{prefix}_{canonical_sha256(value)[:length]}"
