from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate_schema_directory(schema_root: Path) -> dict:
    files = sorted(schema_root.glob("*.schema.json"))
    for path in files:
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
    return {"passed": True, "schema_count": len(files)}
