from tools.repository_paths import find_repository_root
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__);A=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_36';S=ROOT/'schemas/legacy/strategy_factory/saed_v4_36';pairs=0
for p in A.glob('GOLDEN_*.JSON'):
 s=S/(p.stem.lower()+'.schema.json');assert s.exists();data=json.loads(p.read_text());schema=json.loads(s.read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(data);assert schema.get('additionalProperties') is False;pairs+=1
assert pairs>=35
print(f'V4-36 contract closure passed: {pairs} closed artifact/schema pairs')
