from __future__ import annotations

import json
from pathlib import Path


def validate_schema_directory(root: Path) -> list[str]:
    errors: list[str] = []
    paths = sorted(root.glob("*.json"))
    if not paths:
        return ["NO_SCHEMAS"]
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"INVALID_JSON:{path.name}:{exc}")
            continue
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"SCHEMA_DRAFT:{path.name}")
        if data.get("type") != "object":
            errors.append(f"SCHEMA_TYPE:{path.name}")
        if not data.get("required"):
            errors.append(f"SCHEMA_REQUIRED:{path.name}")
    return errors
