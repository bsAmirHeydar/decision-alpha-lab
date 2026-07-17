from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,enum,sha256
from .errors import GovernanceError
from .canonical import content_hash,seal
ROLES={"DEPLOYMENT_ENGINEER","MQL5_RUNTIME_REVIEWER","BROKER_OPERATIONS","INDEPENDENT_MODEL_RISK","RISK_OFFICER","SECURITY_KEY_CUSTODIAN","OPERATOR","INDEPENDENT_VALIDATOR"}
def review_bundle(reviews:list[dict],qualification_hash:str)->dict:
 xs=list_of(reviews,"reviews",8);unique(xs,"review_id","reviews");unique(xs,"reviewer_id","reviews");out=[]
 for r in xs:
  exact(r,["review_id","role","reviewer_id","qualification_hash","decision","findings","independent","review_hash"]);enum(r["role"],ROLES,"role")
  if r["qualification_hash"] not in {"PENDING",qualification_hash}:raise GovernanceError("review target mismatch")
  if r["independent"] is not True:raise GovernanceError("independence required")
  x=deepcopy(r);x["qualification_hash"]=qualification_hash;x["review_hash"]=content_hash({k:v for k,v in x.items() if k!="review_hash"});out.append(x)
 roles={x["role"] for x in out};required={"DEPLOYMENT_ENGINEER","MQL5_RUNTIME_REVIEWER","BROKER_OPERATIONS","INDEPENDENT_MODEL_RISK","RISK_OFFICER","SECURITY_KEY_CUSTODIAN","OPERATOR","INDEPENDENT_VALIDATOR"}
 if roles!=required:raise GovernanceError("governance role quorum incomplete")
 ref_ok=all(x["decision"]=="APPROVE_REFERENCE" for x in out)
 return seal({"phase":"SAED_V4_39","reviews":sorted(out,key=lambda z:z["role"]),"role_count":len(roles),"approved_reference":ref_ok,"micro_live_authorized":False,"two_person_live_control_satisfied":False,"research_only":True},"v439_reviews","review_bundle_id","review_bundle_hash")
