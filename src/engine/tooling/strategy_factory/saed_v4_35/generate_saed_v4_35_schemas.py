from __future__ import annotations
from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__);ART=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_35';SCH=ROOT/'schemas/legacy/strategy_factory/saed_v4_35'
def schema_of(v):
    if isinstance(v,dict):return {'type':'object','required':list(v.keys()),'properties':{k:schema_of(x) for k,x in v.items()},'additionalProperties':False}
    if isinstance(v,list):return {'type':'array','items':schema_of(v[0]) if v else {}}
    if isinstance(v,bool):return {'type':'boolean'}
    if isinstance(v,int):return {'type':'integer'}
    if isinstance(v,float):return {'type':'number'}
    if v is None:return {'type':'null'}
    return {'type':'string'}
def main():
    SCH.mkdir(parents=True,exist_ok=True)
    for old in SCH.glob('*.schema.json'):old.unlink()
    for p in sorted(ART.glob('GOLDEN_*.JSON')):
        data=json.loads(p.read_text());s={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':f'https://alpha-lab.local/saed/v4-35/{p.stem.lower()}.schema.json','title':p.stem,'description':'Closed deterministic SAED V4-35 reference artifact schema.',**schema_of(data)}
        (SCH/(p.stem.lower()+'.schema.json')).write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
