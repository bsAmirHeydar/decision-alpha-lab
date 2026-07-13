"""Canonical serialization and identity primitives for UCE-I11.

The experiment DAG, search plans, resource budgets, cache keys, and ledger
entries all use the same closed JSON domain.  This is essential: changing a
behavior-changing parameter without changing identity would contaminate cache,
resume, and reproducibility evidence simultaneously.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .errors import ExperimentError


def canonical_value(value: Any) -> Any:
    if is_dataclass(value):
        return canonical_value(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        return {str(key): canonical_value(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [canonical_value(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ExperimentError(
                "non_finite_canonical_value",
                "canonical artifacts cannot contain NaN or Infinity",
                {"value": repr(value)},
            )
        if value == 0.0:
            return 0.0
        return float(format(value, ".15g"))
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise ExperimentError(
        "unsupported_canonical_type",
        "value cannot be represented in canonical JSON",
        {"type": type(value).__name__},
    )


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonical_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def bytes_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(prefix: str, value: Any, length: int = 24) -> str:
    if not prefix or not prefix.replace("_", "").isalnum():
        raise ExperimentError(
            "invalid_stable_id_prefix",
            "stable-id prefix must be alphanumeric with optional underscores",
            {"prefix": prefix},
        )
    if length < 8 or length > 64:
        raise ExperimentError(
            "invalid_stable_id_length",
            "stable-id digest length must be between 8 and 64",
            {"length": length},
        )
    return f"{prefix}_{canonical_sha256(value)[:length]}"
