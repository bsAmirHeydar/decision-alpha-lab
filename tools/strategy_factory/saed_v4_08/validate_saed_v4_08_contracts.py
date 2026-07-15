from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];sdir=ROOT/'lab/11_strategy_factory/schemas/saed_v4_08';files=sorted(sdir.glob('*.schema.json'))
if len(files)<27:raise SystemExit('insufficient schema count')
for p in files:
 x=json.loads(p.read_text())
 if x.get('additionalProperties') is not False:raise SystemExit(f'open schema: {p}')
 if x.get('$schema')!='https://json-schema.org/draft/2020-12/schema':raise SystemExit(f'wrong draft: {p}')
print(f'{len(files)} closed schemas validated')
