from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .errors import OperationsError


def load_json_object(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise OperationsError("json_read", f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise OperationsError("json_shape", "top-level JSON must be an object")
    return value


def require_closed_keys(value: Mapping[str, Any], required: set[str], optional: set[str] | None = None) -> None:
    optional = optional or set()
    missing = required - set(value)
    unknown = set(value) - required - optional
    if missing:
        raise OperationsError("missing_keys", ",".join(sorted(missing)))
    if unknown:
        raise OperationsError("unknown_keys", ",".join(sorted(unknown)))
