from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__); sys.path.insert(0,str(Path(__file__).resolve().parent))
from schema_validate import validate
ex=ROOT/'examples/legacy/strategy_factory/saed_v4_37'; sch=ROOT/'schemas/legacy/strategy_factory/saed_v4_37'; count=0
for p in sorted(ex.glob('*.example.json')):
 name=p.name.replace('.example.json',''); validate(json.loads(p.read_text()),json.loads((sch/f'{name}.schema.json').read_text())); count+=1
if count<45:raise SystemExit(f'expected >=45 closed contract pairs, got {count}')
print(json.dumps({'phase':'SAED_V4_37','closed_contract_pairs':count,'passed':True}))
