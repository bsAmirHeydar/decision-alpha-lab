from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
def validate_schema_directory(root:Path)->dict:
    errors=[];count=0
    for p in sorted(root.glob("*.schema.json")):
        count+=1
        try:Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:errors.append({"path":p.as_posix(),"error":str(e)})
    if errors:raise ValueError(errors)
    return {"passed":True,"schema_count":count}
def validate_instance(schema_root:Path,name:str,doc:dict)->None:
    schema=json.loads((schema_root/f"{name}.schema.json").read_text(encoding="utf-8"));errs=list(Draft202012Validator(schema).iter_errors(doc))
    if errs:raise ValueError([e.message for e in errs[:20]])
