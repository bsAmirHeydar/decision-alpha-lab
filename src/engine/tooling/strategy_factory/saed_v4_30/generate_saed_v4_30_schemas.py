from __future__ import annotations
import json
from _common import AR,SC,MAP,load

def schema(v):
 if isinstance(v,dict): return {"type":"object","additionalProperties":False,"required":sorted(v),"properties":{k:schema(v[k]) for k in sorted(v)}}
 if isinstance(v,list): return {"type":"array","items":schema(v[0]) if v else {}}
 if isinstance(v,bool): return {"type":"boolean"}
 if isinstance(v,int) and not isinstance(v,bool): return {"type":"integer"}
 if isinstance(v,float): return {"type":"number"}
 if v is None: return {"type":"null"}
 return {"type":"string"}
SC.mkdir(parents=True,exist_ok=True)
for name in MAP.values():
 value=load(AR/name); out=schema(value); out["$schema"]="https://json-schema.org/draft/2020-12/schema"; out["title"]=name.replace(".JSON","")
 (SC/name.replace(".JSON",".SCHEMA.JSON")).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(f"V4-30 schema generation complete: {len(MAP)} closed schemas")
