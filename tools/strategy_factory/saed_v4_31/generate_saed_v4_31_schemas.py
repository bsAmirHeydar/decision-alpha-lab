from __future__ import annotations
import json
from _common import AR,SC,MAP,load

def merge(a,b):
    if a is None: return b
    if b is None: return a
    if a=={} or b=={}: return {}
    if a.get("type")!=b.get("type"): return {}
    kind=a.get("type")
    if kind=="object":
        ap=a.get("properties",{}); bp=b.get("properties",{})
        keys=sorted(set(ap)|set(bp)); props={}
        for key in keys:
            props[key]=merge(ap.get(key),bp.get(key))
        return {"type":"object","additionalProperties":False,"required":sorted(set(a.get("required",[]))&set(b.get("required",[]))),"properties":props}
    if kind=="array": return {"type":"array","items":merge(a.get("items"),b.get("items")) or {}}
    return a

def schema(v):
    if isinstance(v,dict): return {"type":"object","additionalProperties":False,"required":sorted(v),"properties":{k:schema(v[k]) for k in sorted(v)}}
    if isinstance(v,list):
        item=None
        for value in v: item=merge(item,schema(value))
        return {"type":"array","items":item or {}}
    if isinstance(v,bool): return {"type":"boolean"}
    if isinstance(v,int) and not isinstance(v,bool): return {"type":"integer"}
    if isinstance(v,float): return {"type":"number"}
    if v is None: return {"type":"null"}
    return {"type":"string"}

SC.mkdir(parents=True,exist_ok=True)
for name in MAP.values():
    value=load(AR/name); out=schema(value); out["$schema"]="https://json-schema.org/draft/2020-12/schema"; out["title"]=name.replace(".JSON","")
    (SC/name.replace(".JSON",".SCHEMA.JSON")).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(f"V4-31 schema generation complete: {len(MAP)} closed schemas")
