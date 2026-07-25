from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,enum,integer,number
from .errors import CompilerError
from .canonical import content_hash,seal
OPS={"FEATURE","CONST","ADD","SUB","MUL","DIV","GT","GE","LT","LE","EQ","AND","OR","NOT","CLAMP","SELECT","MODEL_LINEAR","DECISION"}

def freeze_policy_graph(v:dict,feature_names:set[str],output_names:set[str])->dict:
 exact(v,["policy_graph_id","version","nodes","entry_node_id","fallback_decision","closed_graph","research_only"])
 if v["closed_graph"] is not True or v["research_only"] is not True:raise CompilerError("policy graph boundary invalid")
 nodes=list_of(v["nodes"],"nodes",8); unique(nodes,"node_id","nodes"); ids={x["node_id"] for x in nodes}; out=[]
 for n in nodes:
  exact(n,["node_id","ordinal","op","inputs","params","output_name"]); integer(n["ordinal"],"ordinal",0); enum(n["op"],OPS,"op"); list_of(n["inputs"],"inputs")
  if any(i not in ids for i in n["inputs"]):raise CompilerError("unknown node input")
  if n["op"]=="FEATURE" and n["params"].get("name") not in feature_names:raise CompilerError("unknown feature")
  if n["op"]=="DECISION" and n["output_name"] not in output_names:raise CompilerError("unknown output")
  x=deepcopy(n); x["node_hash"]=content_hash(x); out.append(x)
 out=sorted(out,key=lambda z:z["ordinal"])
 if [x["ordinal"] for x in out]!=list(range(len(out))):raise CompilerError("node ordinals must be contiguous")
 if v["entry_node_id"] not in ids:raise CompilerError("entry node missing")
 for n in out:
  for dep in n["inputs"]:
   if next(x["ordinal"] for x in out if x["node_id"]==dep)>=n["ordinal"]:raise CompilerError("graph must be topological")
 return seal({**deepcopy(v),"nodes":out,"node_count":len(out),"graph_hash":content_hash(out)},"v438_policy","frozen_graph_id","frozen_graph_hash")
