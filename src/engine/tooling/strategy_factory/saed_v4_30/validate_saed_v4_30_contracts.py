from __future__ import annotations
from _common import AR,SC,MAP,load
from _schema_validator import validate
for name in MAP.values(): validate(load(AR/name),load(SC/name.replace(".JSON",".SCHEMA.JSON")),name)
assert len(list(AR.glob("*.JSON")))==25
assert len(list(SC.glob("*.SCHEMA.JSON")))==25
print("V4-30 contract validation passed: 25 closed schema pairs")
