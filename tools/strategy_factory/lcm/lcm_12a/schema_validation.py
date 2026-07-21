from __future__ import annotations
import json
from pathlib import Path
import jsonschema

def validate_schemas(schema_root:Path):
    errors=[]
    for path in sorted(schema_root.glob("*.schema.json")):
        try:jsonschema.validators.validator_for(json.loads(path.read_text(encoding="utf-8"))).check_schema(json.loads(path.read_text(encoding="utf-8")))
        except Exception as exc:errors.append(f"{path.name}:{exc}")
    return errors
