from __future__ import annotations
import json
from jsonschema import Draft202012Validator
from .question_registry import registry_snapshot,validate_registry
from .policies import SCHEMA_ROOT,POLICY_ROOT
def validate_registry_files()->dict:
    schemas=list(SCHEMA_ROOT.glob('*.json')); policies=list(POLICY_ROOT.glob('*.json'))
    for p in schemas: Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8')))
    for p in policies: json.loads(p.read_text(encoding='utf-8'))
    validate_registry(registry_snapshot())
    return {'passed':True,'schema_count':len(schemas),'policy_count':len(policies),'question_count':len(registry_snapshot()['entries'])}
