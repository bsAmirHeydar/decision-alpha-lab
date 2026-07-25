from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = frozenset(
    {
        ".bat",
        ".cmd",
        ".conf",
        ".csv",
        ".html",
        ".ini",
        ".json",
        ".md",
        ".ps1",
        ".py",
        ".toml",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)
HASH_POLICY = "TEXT_LF_CANONICAL_BINARY_RAW_V1"


def canonical_file_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.suffix.casefold() not in TEXT_EXTENSIONS:
        return raw
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_file_digest(path: Path) -> str:
    return hashlib.sha256(canonical_file_bytes(path)).hexdigest()


def snapshot_prefixes(root: Path, prefixes: Iterable[str]) -> tuple[str, dict[str, str]]:
    hashes: dict[str, str] = {}
    for prefix in prefixes:
        base = root / prefix
        if not base.exists():
            continue
        for path in sorted(
            item
            for item in base.rglob("*")
            if item.is_file()
            and "__pycache__" not in item.parts
            and ".pytest_cache" not in item.parts
        ):
            hashes[path.relative_to(root).as_posix()] = canonical_file_digest(path)
    snapshot_hash = hashlib.sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return snapshot_hash, hashes
