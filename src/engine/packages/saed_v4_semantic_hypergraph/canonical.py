from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable


def primitive(value: Any) -> Any:
    """Convert supported immutable contract objects into canonical primitives."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return primitive(asdict(value))
    if isinstance(value, dict):
        return {str(k): primitive(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [primitive(v) for v in value]
    if isinstance(value, set):
        return sorted(primitive(v) for v in value)
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        primitive(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def content_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def stable_id(prefix: str, payload: Any, length: int = 24) -> str:
    return f"{prefix}_{content_hash(payload)[:length]}"


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def normalize_time(value: str) -> str:
    return parse_time(value).isoformat(timespec="microseconds").replace("+00:00", "Z")


def merkle_root(leaves: Iterable[str]) -> str:
    level = [sha256_text(leaf) for leaf in sorted(leaves)]
    if not level:
        return sha256_text("")
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [sha256_text(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]
