from __future__ import annotations
import copy,json
from _common import AR,SC,MAP,load
from _schema_validator import validate
for name in MAP.values():
 artifact=load(AR/name); schema=load(SC/name.replace(".JSON",".SCHEMA.JSON")); validate(artifact,schema)
 mutated=copy.deepcopy(artifact); mutated["__unknown_field__"]=True
 try: validate(mutated,schema)
 except AssertionError: pass
 else: raise AssertionError(f"unknown field accepted: {name}")
print(f"V4-31 closed-contract validation passed: {len(MAP)} schema pairs")
