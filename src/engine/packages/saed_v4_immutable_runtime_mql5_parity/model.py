from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,number,sorted_unique_strings
from .errors import CompilerError
from .canonical import content_hash,seal

def freeze_linear_model(v:dict,feature_names:set[str])->dict:
 exact(v,["model_id","model_type","version","features","weights","bias","output_name","training_artifact_hash","research_only"])
 if v["model_type"]!="LINEAR_REFERENCE" or v["research_only"] is not True:raise CompilerError("model boundary invalid")
 fs=sorted_unique_strings(v["features"],"features",1)
 if not set(fs)<=feature_names:raise CompilerError("model feature unavailable")
 ws=list_of(v["weights"],"weights",len(fs))
 if len(ws)!=len(fs):raise CompilerError("weights length mismatch")
 for x in ws:number(x,"weight",-1000,1000)
 number(v["bias"],"bias",-1000,1000)
 x=deepcopy(v); x["features"]=fs; x["model_hash"]=content_hash(x); return seal(x,"v438_model","frozen_model_id","frozen_model_hash")

def score(model:dict,features:dict)->float:return float(model["bias"]+sum(float(w)*float(features[f]) for f,w in zip(model["features"],model["weights"])))
