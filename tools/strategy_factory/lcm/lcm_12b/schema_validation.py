from __future__ import annotations
import json
from pathlib import Path

def validate_schema_directory(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"INVALID_JSON:{path.name}:{exc}")
            continue
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"SCHEMA_DRAFT:{path.name}")
        if data.get("type") != "object":
            errors.append(f"SCHEMA_TYPE:{path.name}")
    return errors
