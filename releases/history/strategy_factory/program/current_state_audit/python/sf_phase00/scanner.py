from __future__ import annotations

import hashlib
from pathlib import Path

from .models import FileRecord
from .scope import is_phase00_self_path


TEXT_EXTENSIONS = {
    ".py", ".md", ".yaml", ".yml", ".json", ".csv", ".txt", ".toml",
    ".ini", ".cfg", ".mq5", ".mqh", ".ps1", ".sh", ".gitignore",
}

IGNORED_DIRS = {".git", ".idea", ".vscode", "node_modules", "__pycache__"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    if path.name in {"LICENSE", "README", ".gitignore"}:
        return True
    try:
        sample = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\x00" not in sample


def _category(relative: str, suffix: str) -> str:
    normalized = relative.replace("\\", "/")
    if "/cache_" in f"/{normalized}" or normalized.startswith("data/"):
        return "generated_or_market_data"
    if suffix in {".parquet", ".feather", ".h5"}:
        return "generated_or_market_data"
    if normalized.startswith("docs/") or suffix == ".md":
        return "documentation"
    if normalized.startswith("registry/") or suffix in {".yaml", ".yml", ".json"}:
        return "registry_or_config"
    if suffix == ".py":
        return "python_source"
    if suffix in {".mq5", ".mqh"}:
        return "mql5_source"
    if suffix == ".pyc" or "__pycache__" in normalized or normalized.startswith(".pytest_cache/"):
        return "ephemeral"
    return "other"


def scan_files(repo_root: Path) -> list[FileRecord]:
    records: list[FileRecord] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(repo_root).parts
        if any(part in IGNORED_DIRS for part in relative_parts):
            continue
        relative = path.relative_to(repo_root).as_posix()
        if is_phase00_self_path(relative):
            continue
        is_text = _is_text(path)
        line_count: int | None = None
        if is_text:
            try:
                line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                line_count = None
        suffix = path.suffix.lower()
        records.append(
            FileRecord(
                path=relative,
                extension=suffix or "[none]",
                size_bytes=path.stat().st_size,
                line_count=line_count,
                sha256=_sha256(path),
                is_binary=not is_text,
                is_empty=path.stat().st_size == 0,
                category=_category(relative, suffix),
            )
        )
    return records
