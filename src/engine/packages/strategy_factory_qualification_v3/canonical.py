from __future__ import annotations

import dataclasses
import enum
import hashlib
import json
import math
from typing import Any

from .errors import QualificationError


def _normalize(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return _normalize(dataclasses.asdict(value))
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise QualificationError("non_finite", "non-finite numbers are forbidden")
        return 0.0 if value == 0.0 else float(format(value, ".12g"))
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def validate_sha256(value: str, field: str = "sha256") -> None:
    if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise QualificationError("invalid_hash", f"{field} must be lowercase SHA-256")
