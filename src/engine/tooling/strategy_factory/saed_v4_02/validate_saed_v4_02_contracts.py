from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__);files=sorted((ROOT/'schemas/legacy/strategy_factory/saed_v4_02').glob('*.schema.json'))
for p in files:
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s)
 if s.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
print(f'validated {len(files)} closed schemas')
