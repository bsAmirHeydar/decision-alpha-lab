import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[4];A=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_36';S=ROOT/'lab/11_strategy_factory/schemas/saed_v4_36'
def test_all_golden_artifacts_have_closed_schema():
    pairs=0
    for p in A.glob('GOLDEN_*.JSON'):
        s=S/(p.stem.lower()+'.schema.json');assert s.exists();data=json.loads(p.read_text());schema=json.loads(s.read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(data);assert schema.get('additionalProperties') is False;pairs+=1
    assert pairs>=35
