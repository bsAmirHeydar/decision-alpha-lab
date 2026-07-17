from __future__ import annotations
import json
from pathlib import Path

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
  if not isinstance(v,dict):raise ValueError(f"{path}: expected object")
  req=set(s["required"])
  if set(v)!=req:raise ValueError(f"{path}: fields mismatch missing={sorted(req-set(v))} unknown={sorted(set(v)-req)}")
  for k in req:validate(v[k],s["properties"][k],path+"."+k)
 elif t=="array":
  if not isinstance(v,list):raise ValueError(f"{path}: expected array")
  for i,x in enumerate(v):validate(x,s["items"],f"{path}[{i}]")
 elif t=="boolean" and not isinstance(v,bool):raise ValueError(path)
 elif t=="integer" and (not isinstance(v,int) or isinstance(v,bool)):raise ValueError(path)
 elif t=="number" and (not isinstance(v,(int,float)) or isinstance(v,bool)):raise ValueError(path)
 elif t=="null" and v is not None:raise ValueError(path)
 elif t=="string" and not isinstance(v,str):raise ValueError(path)
