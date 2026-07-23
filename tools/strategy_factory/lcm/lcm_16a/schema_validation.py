from __future__ import annotations

import json
from pathlib import Path

from jsonschema.validators import validator_for


def validate_schemas(schema_root: Path) -> int:
    count = 0
    for path in sorted(schema_root.glob("*.schema.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        validator = validator_for(document)
        validator.check_schema(document)
        count += 1
    if count < 12:
        raise ValueError("insufficient LCM-16A schemas")
    return count
