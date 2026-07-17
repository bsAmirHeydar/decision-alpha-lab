import json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4];EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_41';SC=ROOT/'lab/11_strategy_factory/schemas/saed_v4_41'
PAIRS=sorted(p.stem.replace('.example','') for p in EX.glob('*.example.json'))
def validate(v,s):
 if 'anyOf' in s:
  errors=[]
  for option in s['anyOf']:
   try:validate(v,option);return
   except (AssertionError,KeyError,TypeError) as exc:errors.append(exc)
  raise AssertionError(f'no anyOf variant matched: {errors}')
 t=s.get('type')
 if t=='object':
  assert isinstance(v,dict);assert set(v)==set(s['required']);assert s['additionalProperties'] is False
  for k,x in v.items():validate(x,s['properties'][k])
 elif t=='array':
  assert isinstance(v,list)
  for x in v:validate(x,s['items'])
 elif t=='boolean':assert isinstance(v,bool)
 elif t=='integer':assert isinstance(v,int) and not isinstance(v,bool)
 elif t=='number':assert isinstance(v,(int,float)) and not isinstance(v,bool)
 elif t=='null':assert v is None
 elif t=='string':assert isinstance(v,str)
@pytest.mark.parametrize('name',PAIRS)
def test_closed_schema_pair(name):
 v=json.loads((EX/f'{name}.example.json').read_text());s=json.loads((SC/f'{name}.schema.json').read_text());assert s['closed_contract'] is True;validate(v,s)
def test_pair_count():assert len(PAIRS)>=45
