"""Canonical serialization and SHA-256 identity primitives for FP-I02."""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Mapping

from .errors import FPI02Error

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$")
_IDENTIFIER_RE = re.compile(r"^[A-Z0-9][A-Z0-9._:@/-]{0,127}$")


def require_sha256(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise FPI02Error("FP_RC_INVALID_SHA256", f"{field} must be lowercase SHA-256", {"field": field})
    return value


def require_semver(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SEMVER_RE.fullmatch(value):
        raise FPI02Error("FP_RC_INVALID_SEMVER", f"{field} must be semantic version", {"field": field})
    return value


def require_identifier(value: str, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER_RE.fullmatch(value):
        raise FPI02Error("FP_RC_INVALID_IDENTIFIER", f"{field} is not a canonical identifier", {"field": field})
    return value


def canonical_value(value: Any) -> Any:
    if is_dataclass(value):
        return canonical_value(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): canonical_value(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [canonical_value(item) for item in value]
    if isinstance(value, set):
        return sorted((canonical_value(item) for item in value), key=lambda item: canonical_json(item))
    if isinstance(value, float):
        if not math.isfinite(value):
            raise FPI02Error("FP_RC_NONFINITE_NUMBER", "non-finite numbers are forbidden")
        if value == 0.0:
            return 0.0
        return float(format(value, ".15g"))
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise FPI02Error("FP_RC_UNSUPPORTED_CANONICAL_TYPE", f"unsupported canonical type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_value(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, value: Any, width: int = 24) -> str:
    if not prefix or not prefix.replace("_", "").isalnum():
        raise FPI02Error("FP_RC_INVALID_ID_PREFIX", "ID prefix must be alphanumeric/underscore")
    if width < 16 or width > 64:
        raise FPI02Error("FP_RC_INVALID_ID_WIDTH", "ID width must be in [16,64]")
    return f"{prefix}_{canonical_sha256(value)[:width]}"


def semantic_hash(value: Any) -> str:
    return canonical_sha256({"identity_domain": "FP_SEMANTIC", "payload": value})


def projection_hash(value: Any) -> str:
    return canonical_sha256({"identity_domain": "FP_PROJECTION", "payload": value})
