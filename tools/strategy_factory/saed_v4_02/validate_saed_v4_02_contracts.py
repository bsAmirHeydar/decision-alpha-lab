from pathlib import Path
import json,sys
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[3];files=sorted((ROOT/'lab/11_strategy_factory/schemas/saed_v4_02').glob('*.schema.json'))
for p in files:
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s)
 if s.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
print(f'validated {len(files)} closed schemas')
