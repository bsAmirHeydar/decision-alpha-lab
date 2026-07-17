import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[3];A=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_35';S=ROOT/'lab/11_strategy_factory/schemas/saed_v4_35';pairs=0
for p in A.glob('GOLDEN_*.JSON'):
 s=S/(p.stem.lower()+'.schema.json');assert s.exists();data=json.loads(p.read_text());schema=json.loads(s.read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(data);assert schema.get('additionalProperties') is False;pairs+=1
assert pairs>=40
print(f'V4-35 contract closure passed: {pairs} closed artifact/schema pairs')
