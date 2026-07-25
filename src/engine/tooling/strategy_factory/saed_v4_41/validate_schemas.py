from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);ex=ROOT/'examples/legacy/strategy_factory/saed_v4_41';sch=ROOT/'schemas/legacy/strategy_factory/saed_v4_41';ps=sorted(ex.glob('*.example.json'));assert len(ps)>=45
for p in ps:
 s=sch/(p.stem.replace('.example','')+'.schema.json');assert s.exists();x=json.loads(s.read_text());assert x['closed_contract'] is True and x['additionalProperties'] is False
print(f'SAED V4-41 schemas: {len(ps)} closed pairs passed')
