"""Deterministic IO helpers used by UC-01."""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
from pathlib import Path
from typing import Iterable, Mapping, Any


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any, *, pretty: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if pretty:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        path.write_text(text, encoding="utf-8", newline="\n")
    else:
        path.write_bytes(canonical_json_bytes(value))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl_gz(path: Path, rows: Iterable[Mapping[str, Any]]) -> tuple[int, str]:
    """Write sorted/canonical caller-provided rows with reproducible gzip metadata."""
    path.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()
    count = 0
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0) as gz:
        for row in rows:
            gz.write(canonical_json_bytes(dict(row)))
            count += 1
    data = buffer.getvalue()
    path.write_bytes(data)
    return count, hashlib.sha256(data).hexdigest()


def iter_jsonl_gz(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def sha256_file(path: Path, *, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def safe_read_text(path: Path, *, max_bytes: int = 8 * 1024 * 1024) -> tuple[str | None, str | None]:
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return None, "text_size_limit_exceeded"
        raw = path.read_bytes()
        if b"\x00" in raw[:4096]:
            return None, "binary_nul_detected"
        return raw.decode("utf-8"), None
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig"), None
        except Exception as exc:  # pragma: no cover - defensive
            return None, f"decode_error:{type(exc).__name__}"
    except Exception as exc:
        return None, f"read_error:{type(exc).__name__}"


def path_mode(path: Path) -> str:
    try:
        return oct(path.lstat().st_mode & 0o777)
    except OSError:
        return "unknown"


def is_probable_lfs_pointer(path: Path) -> bool:
    try:
        if path.stat().st_size > 4096:
            return False
        first = path.open("rb").readline().decode("ascii", errors="ignore").strip()
        return first == "version https://git-lfs.github.com/spec/v1"
    except OSError:
        return False


def redact_url(url: str) -> str:
    """Remove URL userinfo while preserving host and path for provenance."""
    if "://" not in url:
        return url
    scheme, rest = url.split("://", 1)
    if "@" in rest:
        rest = rest.split("@", 1)[1]
    return f"{scheme}://{rest}"


def atomic_replace(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_bytes(data)
    os.replace(temp, path)
