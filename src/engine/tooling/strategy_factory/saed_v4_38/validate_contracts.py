from tools.repository_paths import find_repository_root
import json,sys
from pathlib import Path
ROOT=find_repository_root(__file__);sys.path.insert(0,str(Path(__file__).resolve().parent));from schema_validate import validate
EX=ROOT/'examples/legacy/strategy_factory/saed_v4_38';SCH=ROOT/'schemas/legacy/strategy_factory/saed_v4_38';count=0
for p in sorted(EX.glob('*.example.json')):
 name=p.name.replace('.example.json','');validate(json.loads(p.read_text()),json.loads((SCH/f'{name}.schema.json').read_text()));count+=1
if count<50:raise SystemExit(f'expected >=50 pairs, got {count}')
print(json.dumps({'phase':'SAED_V4_38','closed_contract_pairs':count,'passed':True}))
