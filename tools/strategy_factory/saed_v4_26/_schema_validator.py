from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import jsonschema
def validate(instance_path:Path,schema_path:Path):
 instance=json.loads(instance_path.read_text(encoding="utf-8")); schema=json.loads(schema_path.read_text(encoding="utf-8")); jsonschema.Draft202012Validator.check_schema(schema); jsonschema.validate(instance=instance,schema=schema,cls=jsonschema.Draft202012Validator)
def closed_objects(schema:Any)->bool:
 if isinstance(schema,dict):
  if schema.get("type")=="object" and schema.get("additionalProperties") is not False: return False
  return all(closed_objects(v) for v in schema.values())
 if isinstance(schema,list): return all(closed_objects(v) for v in schema)
 return True
