import json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate(schema_root:Path,package_root:Path):
    errors=[];count=0
    for p in sorted(schema_root.glob("*.schema.json")):
        schema=json.loads(p.read_text(encoding="utf-8"));Draft202012Validator.check_schema(schema);count+=1
    return {"schema_count":count,"schema_instance_count":0,"errors":errors,"passed":not errors}
