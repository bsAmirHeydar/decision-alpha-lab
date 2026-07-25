from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__);sdir=ROOT/'schemas/legacy/strategy_factory/saed_v4_08';files=sorted(sdir.glob('*.schema.json'))
if len(files)<27:raise SystemExit('insufficient schema count')
for p in files:
 x=json.loads(p.read_text())
 if x.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
 if x.get('$schema')!='https://json-schema.org/draft/2020-12/schema':raise SystemExit(f'wrong draft: {p}')
print(f'{len(files)} closed schemas validated')
