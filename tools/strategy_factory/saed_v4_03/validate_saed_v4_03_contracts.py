from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[3]
paths=sorted((ROOT/'lab/11_strategy_factory/schemas/saed_v4_03').glob('*.schema.json'))
for p in paths:
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s)
 if s.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
print(f'validated {len(paths)} closed schemas')
