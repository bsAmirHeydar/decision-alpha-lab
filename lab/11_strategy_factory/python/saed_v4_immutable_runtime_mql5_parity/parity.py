from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique
from .errors import ParityError,RuntimeError438
from .runtime import evaluate
from .numeric import close
from .canonical import content_hash,seal

def freeze_vectors(vectors:list[dict],cutoff:str)->dict:
 vectors=list_of(vectors,"vectors",24); unique(vectors,"vector_id","vectors"); out=[]
 for x in vectors:
  exact(x,["vector_id","known_time","features","expected_decision","expected_treatment_id","expected_confidence","expected_net_edge_bps","expected_size_fraction","synthetic_fixture"])
  if x["known_time"]>cutoff:raise ParityError("future vector")
  y=deepcopy(x); y["vector_hash"]=content_hash(y); out.append(y)
 return seal({"phase":"SAED_V4_38","cutoff_time":cutoff,"vectors":sorted(out,key=lambda z:z["vector_id"]),"vector_count":len(out),"research_only":True},"v438_vectors","vector_set_id","vector_set_hash")

def mql5_reference_emulator(graph:dict,model:dict,features:dict,feature_abi:dict,state:dict)->dict:
 # Intentionally independent expression order matching generated MQL5 source.
 names=[f["name"] for f in feature_abi["fields"]]; arr=[float(features[n]) for n in names]
 score=float(model["bias"])
 for i,w in enumerate(model["weights"]):score=float(score+float(w)*arr[i])
 score=round(score,8); net=round(arr[6]-arr[7],8)
 allowed=arr[11]<=0.20 and arr[8]<=0.80 and net>=3.0 and arr[9]>=0.05 and arr[9]<=0.95 and arr[10]<=0.70 and score>=0.55
 return {"decision":"SELECT" if allowed else "ABSTAIN","treatment_id":"TRT_RUNTIME_REFERENCE" if allowed else "BASELINE","confidence":round(max(0,min(1,score)),8) if allowed else 0.0,"net_edge_bps":net,"size_fraction":round(max(0,min(1,score))*0.25,8) if allowed else 0.0,"reason":"POLICY_ACCEPTED" if allowed else "FAIL_CLOSED_FALLBACK","research_only":True,"order_submission_allowed":False,"capital_activation_allowed":False}

def run_synthetic_parity(vectors:dict,graph:dict,model:dict,feature_abi:dict,state:dict,numeric:dict)->dict:
 rows=[]; exact_count=0; tolerance_count=0; mismatches=0
 for x in vectors["vectors"]:
  py=evaluate(graph,model,x["features"],feature_abi,state); mq=mql5_reference_emulator(graph,model,x["features"],feature_abi,state)
  same_discrete=all(py[k]==mq[k] for k in ["decision","treatment_id","reason","research_only","order_submission_allowed","capital_activation_allowed"])
  nums=["confidence","net_edge_bps","size_fraction"]; exact_num=all(py[k]==mq[k] for k in nums); tolerant=all(close(py[k],mq[k],numeric) for k in nums)
  status="EXACT" if same_discrete and exact_num else "WITHIN_TOLERANCE" if same_discrete and tolerant else "MISMATCH"
  exact_count+=status=="EXACT"; tolerance_count+=status=="WITHIN_TOLERANCE"; mismatches+=status=="MISMATCH"
  rows.append({"vector_id":x["vector_id"],"python_decision":py,"mql5_emulator_decision":mq,"status":status})
 return seal({"phase":"SAED_V4_38","parity_kind":"SYNTHETIC_MQL5_SEMANTIC_EMULATOR","rows":rows,"vector_count":len(rows),"exact_count":exact_count,"within_tolerance_count":tolerance_count,"mismatch_count":mismatches,"passed":mismatches==0,"actual_metaeditor_compile_evidence":False,"actual_terminal_runtime_evidence":False,"research_only":True},"v438_parity","parity_report_id","parity_report_hash")
