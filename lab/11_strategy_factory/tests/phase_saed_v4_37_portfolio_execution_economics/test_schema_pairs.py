import json,pytest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_37'; SCH=ROOT/'lab/11_strategy_factory/schemas/saed_v4_37'

def validate(v,s,path="$"):
 t=s.get("type")
 if isinstance(t,list):
  errors=[]
  for candidate in t:
   try:
    validate(v,{**s,"type":candidate},path); return
   except (AssertionError,ValueError) as exc: errors.append(str(exc))
  raise AssertionError(path) if "pytest" in globals() else ValueError(path)
 if t=="object":
  assert isinstance(v,dict),path; assert set(v)==set(s["required"]),path
  for k in s["required"]:validate(v[k],s["properties"][k],path+"."+k)
 elif t=="array":
  assert isinstance(v,list),path
  for i,x in enumerate(v):validate(x,s["items"],f"{path}[{i}]")
 elif t=="boolean":assert isinstance(v,bool),path
 elif t=="integer":assert isinstance(v,int) and not isinstance(v,bool),path
 elif t=="number":assert isinstance(v,(int,float)) and not isinstance(v,bool),path
 elif t=="null":assert v is None,path
 elif t=="string":assert isinstance(v,str),path
PAIRS=sorted((p.stem.replace('.example',''),p) for p in EX.glob('*.example.json'))
@pytest.mark.parametrize("name,path",PAIRS,ids=[x[0] for x in PAIRS])
def test_closed_schema_pair(name,path):
 v=json.loads(path.read_text()); s=json.loads((SCH/f"{name}.schema.json").read_text()); validate(v,s)
