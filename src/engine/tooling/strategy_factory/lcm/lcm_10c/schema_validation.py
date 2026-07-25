from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate_schema_catalog(root:Path)->dict:
    errors=[];count=0
    for p in sorted(root.glob('*.json')):
        try:Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')));count+=1
        except Exception as e:errors.append({'path':p.as_posix(),'error':str(e)})
    return {'schema_count':count,'errors':errors,'result':'PASS' if not errors else 'FAIL'}
