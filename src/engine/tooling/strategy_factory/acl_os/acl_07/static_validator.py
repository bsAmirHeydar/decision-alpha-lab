from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .policies import SCHEMA_ROOT,POLICY_ROOT

def validate_registry_files()->dict:
    schemas=list(SCHEMA_ROOT.glob('*.schema.json')); policies=list(POLICY_ROOT.glob('*.json'))
    for p in schemas: Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')))
    for p in policies: json.loads(p.read_text(encoding='utf-8'))
    return {'schema_count':len(schemas),'policy_count':len(policies),'passed':True}
