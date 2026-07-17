from __future__ import annotations
from .contracts import exact,list_of,unique
from .errors import GovernanceError
from .canonical import seal,merkle_root,content_hash
def review_bundle(reviews:list[dict])->dict:
 required={"FLEET_ARCHITECT","DATA_GOVERNANCE","MODEL_RISK","SECURITY","SRE","MQL5_RUNTIME","INDEPENDENT_REPLICATION","UCEE_AUTHORITY"}
 list_of(reviews,"reviews",8);unique(reviews,"reviewer_id","reviews");roles=set();rows=[]
 for r in reviews:
  exact(r,["reviewer_id","role","decision","independent","conflicts_declared","scope","evidence_hash"])
  if r["independent"] is not True or r["conflicts_declared"] is not True or r["decision"]!="ACCEPT_REFERENCE":raise GovernanceError("review invalid")
  roles.add(r["role"]);rows.append(r)
 if roles!=required:raise GovernanceError("review role coverage mismatch")
 return seal({"phase":"SAED_V4_40","reviews":sorted(rows,key=lambda z:z["role"]),"roles":sorted(roles),"accepted_reference":True,"production_authorized":False,"research_only":True},"v440_reviews","review_bundle_id","review_bundle_hash")
def evidence_bundle(artifacts:dict,reviews:dict)->dict:
 leaves=[{"name":k,"artifact_hash":v.get(next((x for x in v if x.endswith('_hash')),''),content_hash(v)) if isinstance(v,dict) else content_hash(v)} for k,v in sorted(artifacts.items())]
 hashes=[content_hash(x) for x in leaves]+[reviews["review_bundle_hash"]]
 return seal({"phase":"SAED_V4_40","leaves":leaves,"leaf_count":len(leaves),"review_bundle_hash":reviews["review_bundle_hash"],"evidence_merkle_root":merkle_root(hashes),"external_scale_evidence_complete":False,"actual_hundred_context_soak_passed":False,"actual_multi_terminal_failover_passed":False,"research_only":True,"production_authorized":False},"v440_evidence","evidence_bundle_id","evidence_bundle_hash")
