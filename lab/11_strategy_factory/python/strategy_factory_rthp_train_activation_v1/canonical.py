from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any


def _material(value: Any) -> Any:
    if is_dataclass(value):
        return _material(asdict(value))
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _material(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (list, tuple)):
        return [_material(v) for v in value]
    if isinstance(value, Path):
        return value.as_posix()
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_material(value), ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_material(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(prefix: str, value: Any, length: int = 32, uppercase: bool = False) -> str:
    digest = sha256_material(value)[:length]
    if uppercase:
        digest = digest.upper()
    return f"{prefix}{digest}"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_material(value), ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]] | tuple[dict[str, Any], ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(canonical_json(row))
            stream.write("\n")
