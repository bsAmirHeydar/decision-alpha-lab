from __future__ import annotations
from _common import AR,SC,MAP,load
from _schema_validator import validate
for name in MAP.values(): validate(load(AR/name),load(SC/name.replace(".JSON",".SCHEMA.JSON")))
assert len(list(SC.glob("*.SCHEMA.JSON")))==len(MAP)
print(f"V4-33 contracts passed: {len(MAP)} exact schema pairs")
