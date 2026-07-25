from tools.repository_paths import find_repository_root
from pathlib import Path
import json
from jsonschema import Draft202012Validator
ROOT=find_repository_root(__file__);folder=ROOT/'schemas/legacy/strategy_factory/saed_v4_04'
files=sorted(folder.glob('*.schema.json'))
for p in files:
 d=json.loads(p.read_text());Draft202012Validator.check_schema(d)
 if d.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
print(f'validated {len(files)} closed schemas')
