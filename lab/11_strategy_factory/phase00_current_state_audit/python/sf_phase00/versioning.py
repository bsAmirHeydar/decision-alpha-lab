from __future__ import annotations

from typing import Any


def major_version(version: str) -> int:
    try:
        return int(version.split(".", 1)[0])
    except (AttributeError, ValueError) as exc:
        raise ValueError(f"Invalid semantic version: {version!r}") from exc


def validate_schema_version(document: dict[str, Any], expected_major: int = 1) -> None:
    version = document.get("schema_version")
    if version is None:
        raise ValueError("Missing schema_version")
    actual = major_version(str(version))
    if actual != expected_major:
        raise ValueError(f"Schema major mismatch: expected {expected_major}, got {actual}")
