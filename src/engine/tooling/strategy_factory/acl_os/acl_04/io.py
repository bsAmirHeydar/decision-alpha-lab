from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path
from typing import Any
import yaml
from .errors import SecurityBoundaryError


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_document(path: Path) -> Any:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json(path)
    if suffix in {".yaml", ".yml"}:
        return load_yaml(path)
    raise ValueError(f"unsupported document format: {path}")


def ensure_contained(root: Path, path: Path, *, must_exist: bool = True) -> Path:
    root = root.resolve()
    candidate = path.resolve(strict=False)
    if candidate != root and root not in candidate.parents:
        raise SecurityBoundaryError(f"path escapes root: {candidate}")
    cursor = candidate if candidate.exists() else candidate.parent
    while cursor != root and root in cursor.parents:
        if cursor.is_symlink():
            raise SecurityBoundaryError(f"symlink is forbidden: {cursor}")
        cursor = cursor.parent
    if must_exist and not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def dump_json(path: Path, value: Any) -> None:
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n")


def dump_text(path: Path, value: str) -> None:
    atomic_write(path, value.encode("utf-8"))
