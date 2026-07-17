from __future__ import annotations
import copy,json
from _common import AR,SC,MAP,load
from _schema_validator import validate,ValidationError
for name in MAP.values():
    data=load(AR/name); schema=load(SC/name.replace(".JSON",".SCHEMA.JSON")); validate(data,schema)
    if isinstance(data,dict):
        bad=copy.deepcopy(data);bad["__unknown__"]=1
        try:validate(bad,schema)
        except ValidationError:pass
        else:raise AssertionError(f"unknown field accepted: {name}")
print(f"V4-34 contract validation passed: {len(MAP)} closed schema pairs")
