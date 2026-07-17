from __future__ import annotations
from collections import defaultdict
from .canonical import seal,hash_chain,content_hash
from .errors import RetirementError,GovernanceError
REQUIRED_STATES=["PROPOSED","EVIDENCE_FROZEN","IMPACT_REVIEWED","APPROVED","ROUTES_REVOKED","TOMBSTONED","ARCHIVED","VERIFIED_RETIRED"]
def compile_retirements(fusion:dict,registry:dict,policy:dict,approvals:list[dict],replacement_map:dict,impact:dict,cutoff:str)->dict:
 cells={x["cell_id"]:x for x in registry["cells"]};candidates=[x for x in fusion["rows"] if x["action"]=="RETIRE_CANDIDATE"]
 allowed_roles=set(policy["retirement_approval_roles"]);by=defaultdict(list)
 for a in approvals:
  if set(a)!={"approval_id","cell_id","role","approved","known_time","evidence_hash","synthetic_fixture"}:raise GovernanceError("approval contract invalid")
  if a["synthetic_fixture"] is not True or a["known_time"]>cutoff:raise GovernanceError("approval evidence invalid")
  if a["role"] not in allowed_roles:raise GovernanceError("unknown retirement approval role")
  by[a["cell_id"]].append(a)
 records=[];events=[];pending=[]
 for d in candidates:
  cid=d["cell_id"];c=cells[cid];valid={a["role"] for a in by.get(cid,[]) if a["approved"] and a["role"] in allowed_roles}
  replacement=replacement_map.get(cid)
  eligible=len(valid)>=policy["retirement_min_approvals"] and replacement in cells and cells[replacement]["tenant_id"]==c["tenant_id"] and impact["cross_tenant_impact"] is False
  if not eligible:
   pending.append({"cell_id":cid,"reason":"INSUFFICIENT_APPROVAL_OR_REPLACEMENT","approval_count":len(valid),"required":policy["retirement_min_approvals"],"replacement_cell_id":replacement});continue
  state_events=[];prev=None
  for state in REQUIRED_STATES:
   ev={"retirement_id":f"RET_{cid}","cell_id":cid,"from_state":prev,"to_state":state,"known_time":cutoff,"approved_roles":sorted(valid),"replacement_cell_id":replacement,"live_order_side_effect":False,"capital_effect":0.0}
   state_events.append(ev);events.append(ev);prev=state
  record={"retirement_id":f"RET_{cid}","cell_id":cid,"tenant_id":c["tenant_id"],"namespace":c["namespace"],"context_id":c["context_id"],"context_version":c["context_version"],"model_generation":c["model_generation"],"runtime_bundle_hash":c["runtime_bundle_hash"],"treatment_universe_hash":c["treatment_universe_hash"],"replacement_cell_id":replacement,"approved_roles":sorted(valid),"retired_at":cutoff,"route_revoked":True,"capital_delta":0.0,"order_delta":0,"reinstatement_allowed":False,"requires_new_qualification_for_successor":True,"tombstone_hash":content_hash([cid,c,cutoff,replacement,sorted(valid)]),"final_state":"VERIFIED_RETIRED","synthetic_fixture":True}
  records.append(record)
 return seal({"fusion_hash":fusion["fusion_hash"],"policy_hash":policy["frozen_policy_hash"],"retired_records":records,"pending_candidates":pending,"events":hash_chain(events,"v441_retirement_event"),"candidate_count":len(candidates),"retired_count":len(records),"pending_count":len(pending),"all_retired_routes_revoked":all(x["route_revoked"] for x in records),"reinstatement_without_requalification":False,"live_order_side_effects":0,"capital_delta":0.0,"research_only":True},"v441_retirement","retirement_ledger_id","retirement_ledger_hash")
