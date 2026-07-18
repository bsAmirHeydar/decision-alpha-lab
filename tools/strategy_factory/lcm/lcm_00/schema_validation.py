from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema


def load_schemas(schema_root: Path) -> dict[str, dict]:
    result = {}
    for path in sorted(schema_root.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        result[path.stem.replace(".schema", "")] = schema
    return result


def validate_instance(value: Any, schema: dict) -> None:
    jsonschema.Draft202012Validator(schema).validate(value)
