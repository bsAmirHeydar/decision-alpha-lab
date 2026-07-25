from __future__ import annotations
import json
from jsonschema import Draft202012Validator
from .policies import SCHEMA_ROOT, POLICY_ROOT
from .state_registry import state_registry_snapshot,transition_registry_snapshot,prerequisite_registry_snapshot,validate_registries

def validate_registry_files() -> dict:
    schemas=list(SCHEMA_ROOT.glob('*.json')); policies=list(POLICY_ROOT.glob('*.json'))
    for path in schemas: Draft202012Validator.check_schema(json.loads(path.read_text(encoding='utf-8')))
    for path in policies: json.loads(path.read_text(encoding='utf-8'))
    validate_registries(state_registry_snapshot(),transition_registry_snapshot(),prerequisite_registry_snapshot())
    return {'passed':True,'schema_count':len(schemas),'policy_count':len(policies),'state_count':len(state_registry_snapshot()['states']),'transition_count':len(transition_registry_snapshot()['transitions']),'prerequisite_count':len(prerequisite_registry_snapshot()['prerequisites'])}
