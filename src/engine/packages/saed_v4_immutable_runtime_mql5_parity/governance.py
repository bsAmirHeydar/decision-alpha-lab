from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,enum
from .errors import GovernanceError
from .canonical import content_hash,seal
ROLES={"RUNTIME_ENGINEER","MQL5_REVIEWER","MODEL_RISK","INDEPENDENT_VALIDATOR","SECURITY_REVIEWER"}

def review_bundle(reviews:list[dict],release_hash:str)->dict:
 reviews=list_of(reviews,"reviews",5); unique(reviews,"review_id","reviews"); unique(reviews,"role","review roles"); out=[]
 for x in reviews:
  exact(x,["review_id","role","release_hash","decision","findings","independent","reviewer_id","review_hash"]); enum(x["role"],ROLES,"role"); enum(x["decision"],{"APPROVE_REFERENCE","REJECT"},"decision")
  if x["release_hash"]!=release_hash or x["independent"] is not True:raise GovernanceError("review binding invalid")
  y=deepcopy(x); expected=y.pop("review_hash")
  if expected!=content_hash(y):raise GovernanceError("review hash invalid")
  y["review_hash"]=expected; out.append(y)
 approved=all(x["decision"]=="APPROVE_REFERENCE" for x in out)
 return seal({"phase":"SAED_V4_38","release_hash":release_hash,"reviews":sorted(out,key=lambda z:z["role"]),"role_count":len(out),"approved_reference":approved,"approved_external_runtime":False,"production_authorized":False,"research_only":True},"v438_review","review_bundle_id","review_bundle_hash")
