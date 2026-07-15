from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Iterable


def primitive(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Decimal):
        text = format(value.normalize(), "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text or "0"
    if is_dataclass(value):
        return primitive(asdict(value))
    if isinstance(value, dict):
        return {str(key): primitive(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [primitive(item) for item in value]
    if isinstance(value, set):
        return sorted(primitive(item) for item in value)
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        primitive(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def content_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def stable_id(prefix: str, value: Any, length: int = 24) -> str:
    return f"{prefix}_{content_hash(value)[:length]}"


def merkle_root(leaves: Iterable[str]) -> str:
    level = [sha256_text(item) for item in sorted(leaves)]
    if not level:
        return sha256_text("")
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [sha256_text(level[index] + level[index + 1]) for index in range(0, len(level), 2)]
    return level[0]
