from pathlib import Path
import json,pytest
ROOT=Path(__file__).resolve().parents[4];ART=ROOT/'lab/11_strategy_factory/artifacts/saed_v4_23';EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_23';SCH=ROOT/'lab/11_strategy_factory/schemas/saed_v4_23'
NAMES=sorted([p.stem for p in ART.glob('*.JSON')]+[p.stem for p in EX.glob('*.JSON')])
def validate(v,s,path='$'):
    t=s.get('type')
    if t=='object':
        assert isinstance(v,dict),path;assert set(v)==set(s['required']),path
        for k in s['required']:validate(v[k],s['properties'][k],path+'.'+k)
    elif t=='array':
        assert isinstance(v,list),path
        for i,x in enumerate(v):validate(x,s['items'],f'{path}[{i}]')
    elif t=='boolean':assert isinstance(v,bool),path
    elif t=='integer':assert isinstance(v,int) and not isinstance(v,bool),path
    elif t=='number':assert isinstance(v,(int,float)) and not isinstance(v,bool),path
    elif t=='string':assert isinstance(v,str),path
    elif t=='null':assert v is None,path
@pytest.mark.parametrize('name',NAMES)
def test_closed_schema(name):
    p=(ART/f'{name}.JSON') if (ART/f'{name}.JSON').exists() else (EX/f'{name}.JSON');v=json.loads(p.read_text());s=json.loads((SCH/f'{name}.SCHEMA.JSON').read_text());validate(v,s)
