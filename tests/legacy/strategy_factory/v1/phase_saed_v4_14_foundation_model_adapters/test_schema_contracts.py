import json
from pathlib import Path

def validate(v,s,path='$'):
 t=s.get('type')
 if t=='object':
  assert isinstance(v,dict),path;assert set(v)==set(s.get('required',[])),(path,set(v)^set(s.get('required',[])))
  for k in v:validate(v[k],s['properties'][k],path+'.'+k)
 elif t=='array':
  assert isinstance(v,list),path
  for i,x in enumerate(v):validate(x,s.get('items',{}),f'{path}[{i}]')
 elif t=='boolean':assert isinstance(v,bool)
 elif t=='integer':assert isinstance(v,int) and not isinstance(v,bool)
 elif t=='number':assert isinstance(v,(int,float)) and not isinstance(v,bool)
 elif t=='null':assert v is None
 elif t=='string':assert isinstance(v,str)

def test_all_contract_schema_pairs(root,load):
 m=load('releases/history/strategy_factory/artifacts/saed_v4_14/CONTRACT_VALIDATION_MAP.JSON')
 for row in m['contracts']:
  validate(load(row['document']),load(row['schema']))
