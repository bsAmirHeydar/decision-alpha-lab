from __future__ import annotations
import json
from pathlib import Path


def validate(schema_root: Path) -> dict:
    try:
        from jsonschema.validators import validator_for
    except ImportError:
        return {"passed":False,"reason":"jsonschema unavailable","schema_count":0}
    count=0
    for path in sorted(schema_root.glob('*.schema.json')):
        schema=json.loads(path.read_text(encoding='utf-8'))
        validator=validator_for(schema);validator.check_schema(schema);count+=1
    return {"passed":True,"schema_count":count}
