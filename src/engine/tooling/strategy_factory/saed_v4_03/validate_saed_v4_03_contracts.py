from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__)
paths=sorted((ROOT/'schemas/legacy/strategy_factory/saed_v4_03').glob('*.schema.json'))
for p in paths:
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s)
 if s.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
print(f'validated {len(paths)} closed schemas')
