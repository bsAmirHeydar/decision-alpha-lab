from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_object(value: Any, digest_field: str | None = None) -> str:
    if digest_field and isinstance(value, dict):
        value = {key: item for key, item in value.items() if key != digest_field}
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    """Digest a locator target deterministically.

    LCM locators may resolve to either a single file or a governed package
    directory. Directory identity binds lexical relative paths and file bytes.
    """
    digest = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return "sha256:" + digest.hexdigest()
    if path.is_dir():
        for child in sorted(item for item in path.rglob("*") if item.is_file()):
            digest.update(child.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            with child.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
        return "sha256:" + digest.hexdigest()
    raise FileNotFoundError(path)


def stable_id(prefix: str, *parts: object, length: int = 32) -> str:
    raw = "|".join(str(part) for part in parts)
    return f"{prefix}_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:length].upper()}"


def verify_embedded_digest(value: dict[str, Any], field: str) -> bool:
    return isinstance(value.get(field), str) and value[field] == digest_object(value, field)
