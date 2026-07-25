from __future__ import annotations

from pathlib import Path


FORBIDDEN_API_TOKENS: tuple[str, ...] = (
    "Order" + "Send",
    "Position" + "Open",
    "Position" + "Modify",
    "Position" + "Close",
    "Object" + "Create",
    "Object" + "Set",
    "Chart" + "Redraw",
)


def scan_module(root: Path) -> dict[str, object]:
    """Fail closed when migration tooling contains runtime or drawing APIs."""
    if not root.is_dir():
        raise FileNotFoundError(f"module root does not exist: {root}")

    python_files = sorted(path for path in root.glob("*.py") if path.is_file())
    if not python_files:
        raise RuntimeError(f"no Python modules found under: {root}")

    source_text = "\n".join(
        path.read_text(encoding="utf-8", errors="strict")
        for path in python_files
    )
    hits = sorted(token for token in FORBIDDEN_API_TOKENS if token in source_text)
    if hits:
        raise RuntimeError(f"forbidden API tokens: {hits}")

    return {
        "passed": True,
        "scanned_file_count": len(python_files),
        "forbidden_hit_count": 0,
        "forbidden_tokens": list(FORBIDDEN_API_TOKENS),
    }
