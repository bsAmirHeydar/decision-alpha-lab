from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import ReviewError

CHECK_KEYS=["checkpoint_id","task_id","checkpoint_type","requester_agent_id","reviewer_ids","required_roles","decision","reason","evidence_hashes","known_time_epoch","self_approval","research_only"]
TYPES={"scope_freeze","protected_access","candidate_review","blocking_issue_resolution","incident_closure","handoff_review"}
DECISIONS={"approved_research_only","rejected","quarantined","extension_required"}

def freeze_checkpoints(items:list[dict],agents:dict)->dict:
    require_list(items,"checkpoints",1); require_unique(items,"checkpoint_id","checkpoints")
    by={a["agent_id"]:a for a in agents["agents"]}; rows=[]
    for c in items:
        require_exact(c,CHECK_KEYS,name="checkpoint")
        require_enum(c["checkpoint_type"],TYPES,"checkpoint_type"); require_enum(c["decision"],DECISIONS,"decision")
        if c["requester_agent_id"] not in by or set(c["reviewer_ids"])-set(by): raise ReviewError("unknown checkpoint actor")
        if c["requester_agent_id"] in c["reviewer_ids"] or c["self_approval"] is not False: raise ReviewError("self approval forbidden")
        roles={by[r]["role_id"] for r in c["reviewer_ids"]}
        if set(c["required_roles"])-roles: raise ReviewError("required review role missing")
        if "human_reviewer" not in roles: raise ReviewError("human reviewer required")
        if len(roles)<2: raise ReviewError("independent two-role review required")
        if c["research_only"] is not True: raise ReviewError("research_only required")
        row=deepcopy(c); row["checkpoint_hash"]=content_hash(c); rows.append(row)
    body={"phase":"SAED_V4_32","checkpoints":sorted(rows,key=lambda x:x["checkpoint_id"]),"checkpoint_count":len(rows),"self_approvals":0,"two_person_integrity":True,"human_review_present":True,"research_only":True}
    body["registry_id"]=stable_id("v432_checkpoint_registry",body); body["registry_hash"]=content_hash(body); return body

def quorum_ledger(checkpoints:dict,agents:dict)->dict:
    by={a["agent_id"]:a for a in agents["agents"]}; rows=[]
    for c in checkpoints["checkpoints"]:
        roles=sorted({by[x]["role_id"] for x in c["reviewer_ids"]})
        row={"checkpoint_id":c["checkpoint_id"],"decision":c["decision"],"reviewer_ids":sorted(c["reviewer_ids"]),"independent_roles":roles,"quorum_size":len(c["reviewer_ids"]),"minimum_quorum":2,"quorum_met":len(c["reviewer_ids"])>=2 and len(roles)>=2,"self_approval":False,"live_authority_granted":False}
        if not row["quorum_met"]: raise ReviewError("quorum not met")
        rows.append(row)
    body={"phase":"SAED_V4_32","rows":rows,"all_quorums_met":True,"single_agent_decisions":0,"live_authority_decisions":0,"research_only":True}
    body["ledger_id"]=stable_id("v432_quorum_ledger",body); body["ledger_hash"]=content_hash(body); return body
