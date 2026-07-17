from __future__ import annotations
import json
from _common import AR,SC,MAP
from _schema_validator import validate
assert len(MAP)==38
for name in MAP.values():
    artifact=json.loads((AR/name).read_text()); schema=json.loads((SC/name.replace('.JSON','.SCHEMA.JSON')).read_text())
    assert schema["additionalProperties"] is False
    validate(artifact,schema)
print(f"V4-32 contract validation passed: {len(MAP)} closed artifact/schema pairs")
