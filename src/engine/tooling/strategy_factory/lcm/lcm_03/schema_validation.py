from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate_schemas(schema_root: Path):
    count=0
    for p in sorted(schema_root.glob('*.schema.json')):
        Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')));count+=1
    return count
