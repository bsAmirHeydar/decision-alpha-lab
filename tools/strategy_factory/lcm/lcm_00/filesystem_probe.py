from __future__ import annotations

import mimetypes
import os
import stat
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

from .canonical import normalize_root_relative, sha256_file
from .scope import ScopePolicy, classify_path


def _looks_binary(path: Path, sample_size: int = 8192) -> bool:
    try:
        data = path.read_bytes()[:sample_size]
    except OSError:
        return True
    return b"\x00" in data


def _record(root: Path, rel: str) -> dict:
    path = root / rel
    st = path.lstat()
    is_symlink = path.is_symlink()
    mode = stat.S_IMODE(st.st_mode)
    if is_symlink:
        target = os.readlink(path)
        return {
            "path": rel,
            "kind": "SYMLINK",
            "size_bytes": st.st_size,
            "sha256": None,
            "symlink_target": target,
            "mode_octal": format(mode, "04o"),
            "extension": path.suffix.lower(),
            "binary": False,
        }
    mime, _ = mimetypes.guess_type(path.name)
    return {
        "path": rel,
        "kind": "FILE",
        "size_bytes": st.st_size,
        "sha256": sha256_file(path),
        "symlink_target": None,
        "mode_octal": format(mode, "04o"),
        "extension": path.suffix.lower(),
        "mime_guess": mime,
        "binary": _looks_binary(path),
    }


def collect_scope(root: Path, policy: ScopePolicy, workers: int | None = None) -> tuple[list[dict], list[dict]]:
    included: list[str] = []
    excluded: list[dict] = []
    for path in root.rglob("*"):
        if not (path.is_file() or path.is_symlink()):
            continue
        rel = path.relative_to(root).as_posix()
        allowed, reason = classify_path(rel, policy)
        if allowed:
            included.append(normalize_root_relative(rel))
        else:
            excluded.append({"path": rel, "reason": reason})
    included.sort()
    excluded.sort(key=lambda x: x["path"])
    max_workers = workers or min(32, (os.cpu_count() or 4) + 4)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        records = list(pool.map(lambda r: _record(root, r), included))
    records.sort(key=lambda x: x["path"])
    return records, excluded


def summarize_records(records: list[dict], large_file_threshold: int) -> dict:
    extension_counts: dict[str, int] = {}
    binary_count = 0
    symlink_count = 0
    total_bytes = 0
    large_file_count = 0
    for item in records:
        ext = item.get("extension") or "<none>"
        extension_counts[ext] = extension_counts.get(ext, 0) + 1
        binary_count += int(bool(item.get("binary")))
        symlink_count += int(item["kind"] == "SYMLINK")
        total_bytes += int(item["size_bytes"])
        large_file_count += int(int(item["size_bytes"]) >= large_file_threshold)
    return {
        "file_record_count": len(records),
        "total_bytes": total_bytes,
        "binary_file_count": binary_count,
        "symlink_count": symlink_count,
        "large_file_count": large_file_count,
        "extension_counts": dict(sorted(extension_counts.items())),
    }
