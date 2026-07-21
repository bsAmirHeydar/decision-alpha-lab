from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .errors import ContractError

def validate_instance(schema_root:Path,name:str,instance:dict)->None:
    path=schema_root/f"{name}.schema.json"
    schema=json.loads(path.read_text(encoding="utf-8"));errors=sorted(Draft202012Validator(schema).iter_errors(instance),key=lambda e:list(e.path))
    if errors:raise ContractError("LCM09B_SCHEMA_INVALID:"+name+":"+";".join(e.message for e in errors[:5]))
def validate_schema_directory(schema_root:Path)->dict:
    count=0
    for p in sorted(schema_root.glob("*.schema.json")):
        Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")));count+=1
    return {"passed":True,"schema_count":count}
