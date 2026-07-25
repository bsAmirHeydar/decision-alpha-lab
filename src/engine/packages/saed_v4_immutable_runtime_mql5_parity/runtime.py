from __future__ import annotations
import math
from .errors import RuntimeError438
from .model import score
from .numeric import quantize

def validate_features(features:dict,feature_abi:dict)->dict:
 expected={f["name"] for f in feature_abi["fields"]}; unknown=set(features)-expected; missing=expected-set(features)
 if unknown or missing:raise RuntimeError438(f"feature fields mismatch missing={sorted(missing)} unknown={sorted(unknown)}")
 out={}
 for f in feature_abi["fields"]:
  v=features[f["name"]]
  if f["data_type"]=="FLOAT64":
   if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(float(v)):raise RuntimeError438("invalid float feature")
   if float(v)<float(f["minimum"]) or float(v)>float(f["maximum"]):raise RuntimeError438(f"feature out of bounds: {f['name']}")
   out[f["name"]]=quantize(float(v),8)
  elif f["data_type"]=="BOOL":
   if not isinstance(v,bool):raise RuntimeError438("invalid bool feature")
   out[f["name"]]=v
  else:out[f["name"]]=v
 return out

def evaluate(graph:dict,model:dict,features:dict,feature_abi:dict,state:dict)->dict:
 f=validate_features(features,feature_abi); values={}; decision=None
 for n in graph["nodes"]:
  op=n["op"]; ins=[values[i] for i in n["inputs"]]; p=n["params"]
  if op=="FEATURE":v=f[p["name"]]
  elif op=="CONST":v=p["value"]
  elif op=="ADD":v=ins[0]+ins[1]
  elif op=="SUB":v=ins[0]-ins[1]
  elif op=="MUL":v=ins[0]*ins[1]
  elif op=="DIV":
   if abs(ins[1])<1e-15:raise RuntimeError438("division by zero")
   v=ins[0]/ins[1]
  elif op=="GT":v=ins[0]>ins[1]
  elif op=="GE":v=ins[0]>=ins[1]
  elif op=="LT":v=ins[0]<ins[1]
  elif op=="LE":v=ins[0]<=ins[1]
  elif op=="EQ":v=ins[0]==ins[1]
  elif op=="AND":v=bool(ins[0] and ins[1])
  elif op=="OR":v=bool(ins[0] or ins[1])
  elif op=="NOT":v=not bool(ins[0])
  elif op=="CLAMP":v=max(float(p["minimum"]),min(float(p["maximum"]),float(ins[0])))
  elif op=="SELECT":v=ins[1] if ins[0] else ins[2]
  elif op=="MODEL_LINEAR":v=score(model,f)
  elif op=="DECISION":
   allowed=bool(ins[0]); conf=float(ins[1]); net=float(ins[2]);
   v={"decision":"SELECT" if allowed else graph["fallback_decision"],"treatment_id":p["treatment_id"] if allowed else "BASELINE","confidence":quantize(conf,8) if allowed else 0.0,"net_edge_bps":quantize(net,8),"size_fraction":quantize(max(0.0,min(1.0,conf))*float(p["max_size_fraction"]),8) if allowed else 0.0,"reason":"POLICY_ACCEPTED" if allowed else "FAIL_CLOSED_FALLBACK","research_only":True,"order_submission_allowed":False,"capital_activation_allowed":False}
   decision=v
  else:raise RuntimeError438(f"unknown op {op}")
  values[n["node_id"]]=quantize(v,8) if isinstance(v,float) else v
 if decision is None:raise RuntimeError438("decision node not executed")
 return decision
