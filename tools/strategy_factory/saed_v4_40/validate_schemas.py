import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ex=ROOT/'lab/11_strategy_factory/examples/saed_v4_40';sch=ROOT/'lab/11_strategy_factory/schemas/saed_v4_40';ps=sorted(ex.glob('*.example.json'));assert len(ps)>=50
for p in ps:
 s=sch/(p.stem.replace('.example','')+'.schema.json');assert s.exists();x=json.loads(s.read_text());assert x['closed_contract'] is True
 if x.get('type')=='object':assert x['additionalProperties'] is False
print(f'SAED V4-40 schemas: {len(ps)} closed pairs passed')
