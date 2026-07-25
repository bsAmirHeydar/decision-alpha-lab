import json
from pathlib import Path
import jsonschema
from conftest import ROOT,load

def test_all_schemas_are_closed_objects():
    for p in (ROOT/'schemas/legacy/strategy_factory/saed_v4_09').glob('*.schema.json'):
        s=json.loads(p.read_text());jsonschema.Draft202012Validator.check_schema(s)
        if s.get('type')=='object':assert s.get('additionalProperties') is False

def test_profile_validates_against_schema():
    schema=load('schemas/legacy/strategy_factory/saed_v4_09/execution_twin_profile.schema.json');profile=load('examples/legacy/strategy_factory/saed_v4_09/execution_twin_profile.json');jsonschema.validate(profile,schema)
