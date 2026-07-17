import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(Path(__file__).resolve().parent))
from schema_validate import validate
ex=ROOT/'lab/11_strategy_factory/examples/saed_v4_37'; sch=ROOT/'lab/11_strategy_factory/schemas/saed_v4_37'; count=0
for p in sorted(ex.glob('*.example.json')):
 name=p.name.replace('.example.json',''); validate(json.loads(p.read_text()),json.loads((sch/f'{name}.schema.json').read_text())); count+=1
if count<45:raise SystemExit(f'expected >=45 closed contract pairs, got {count}')
print(json.dumps({'phase':'SAED_V4_37','closed_contract_pairs':count,'passed':True}))
