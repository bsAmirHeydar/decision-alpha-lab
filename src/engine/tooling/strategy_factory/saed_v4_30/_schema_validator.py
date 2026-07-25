from __future__ import annotations
from jsonschema import Draft202012Validator

def validate(instance,schema,name="contract"):
 errors=sorted(Draft202012Validator(schema).iter_errors(instance),key=lambda e:list(e.path))
 if errors:
  details="; ".join(f"{list(e.path)}: {e.message}" for e in errors[:10])
  raise AssertionError(f"{name} schema failure: {details}")
