"""Stable repository-root discovery independent of file depth."""
from __future__ import annotations

from pathlib import Path

_MARKERS = (".git", "pyproject.toml", "README.md")


def find_repository_root(start: str | Path) -> Path:
    """Return the nearest Alpha Lab repository root or fail explicitly."""
    path = Path(start).resolve()
    current = path.parent if path.is_file() else path
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
        if (candidate / "README.md").is_file() and (
            (candidate / "lab").exists()
            or (candidate / "src/engine").exists()
            or (candidate / "releases/unified_consolidation").exists()
        ):
            return candidate
    raise RuntimeError(f"unable to locate Alpha Lab repository root from {start}")
