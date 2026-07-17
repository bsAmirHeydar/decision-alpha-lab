from __future__ import annotations
from .contracts import exact,list_of,unique,sorted_unique_strings
from .errors import GovernanceError
from .canonical import seal,content_hash
ROLES={"SURVEILLANCE_ARCHITECT","DATA_GOVERNANCE","MODEL_RISK","SECURITY","SRE","MQL5_RUNTIME","INDEPENDENT_REPLICATION","UCEE_AUTHORITY"}
def review_bundle(v:dict,evidence_hash:str)->dict:
 exact(v,["review_id","reviews","unresolved_findings","accepted_reference","external_gates_open","research_only"])
 reviews=list_of(v["reviews"],"reviews",8);unique(reviews,"role","reviews")
 if {x["role"] for x in reviews}!=ROLES:raise GovernanceError("review role coverage mismatch")
 for r in reviews:
  exact(r,["role","reviewer_id","decision","evidence_hash","signed","limitations"])
  if r["decision"]!="ACCEPT_REFERENCE" or r["signed"] is not True or r["evidence_hash"]!=evidence_hash:raise GovernanceError("review not accepting bound evidence")
 if v["accepted_reference"] is not True or v["external_gates_open"] is not True or v["research_only"] is not True:raise GovernanceError("review boundary invalid")
 x={**v,"reviews":sorted(reviews,key=lambda z:z["role"]),"review_set_hash":content_hash(reviews)};return seal(x,"v441_review","review_bundle_id","review_bundle_hash")
