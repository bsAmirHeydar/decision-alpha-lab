import json
from pathlib import Path
import jsonschema
from conftest import ROOT,load

def test_all_schemas_are_closed_objects():
    for p in (ROOT/'lab/11_strategy_factory/schemas/saed_v4_09').glob('*.schema.json'):
        s=json.loads(p.read_text());jsonschema.Draft202012Validator.check_schema(s)
        if s.get('type')=='object':assert s.get('additionalProperties') is False

def test_profile_validates_against_schema():
    schema=load('lab/11_strategy_factory/schemas/saed_v4_09/execution_twin_profile.schema.json');profile=load('lab/11_strategy_factory/examples/saed_v4_09/execution_twin_profile.json');jsonschema.validate(profile,schema)
