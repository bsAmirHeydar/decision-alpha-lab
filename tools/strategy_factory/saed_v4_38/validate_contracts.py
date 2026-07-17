import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(Path(__file__).resolve().parent));from schema_validate import validate
EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_38';SCH=ROOT/'lab/11_strategy_factory/schemas/saed_v4_38';count=0
for p in sorted(EX.glob('*.example.json')):
 name=p.name.replace('.example.json','');validate(json.loads(p.read_text()),json.loads((SCH/f'{name}.schema.json').read_text()));count+=1
if count<50:raise SystemExit(f'expected >=50 pairs, got {count}')
print(json.dumps({'phase':'SAED_V4_38','closed_contract_pairs':count,'passed':True}))
