from __future__ import annotations
from copy import deepcopy
from .canonical import seal,hash_chain
from .contracts import require_exact,require_list,require_unique,require_int
from .errors import GovernanceError

def freeze_policy(v:dict)->dict:
    require_exact(v,["policy_id","required_roles","quorum","independent_challenge_required","risk_review_required","negative_knowledge_review_required","automatic_approval_allowed","automatic_execution_allowed","research_only"])
    if sorted(set(v["required_roles"]))!=v["required_roles"]: raise GovernanceError("roles must be sorted unique")
    require_int(v["quorum"],"quorum",2)
    if not all(v[k] is True for k in ["independent_challenge_required","risk_review_required","negative_knowledge_review_required","research_only"]): raise GovernanceError("governance requirements missing")
    if v["automatic_approval_allowed"] or v["automatic_execution_allowed"]: raise GovernanceError("automatic authority forbidden")
    return seal(deepcopy(v)|{"phase":"SAED_V4_36"},"v436_policy","policy_receipt_id","policy_hash")

def review(plan:dict,policy:dict,approvals:list[dict])->dict:
    approvals=require_list(approvals,"approvals",policy["quorum"]); require_unique(approvals,"approval_id","approvals"); roles=set(); rows=[]
    for x in approvals:
        require_exact(x,["approval_id","reviewer_id","role","decision","independent","reviewed_plan_hash","negative_knowledge_reviewed","risk_findings_reviewed","synthetic_fixture"])
        if x["reviewed_plan_hash"]!=plan["plan_hash"]: raise GovernanceError("approval bound to wrong plan")
        if x["decision"] not in ["APPROVE_REFERENCE","REJECT","REQUEST_CHANGE"]: raise GovernanceError("decision invalid")
        roles.add(x["role"]); rows.append(deepcopy(x))
    role_ok=set(policy["required_roles"])<=roles; quorum=len(rows)>=policy["quorum"]; independent=any(x["independent"] for x in rows); all_approve=all(x["decision"]=="APPROVE_REFERENCE" for x in rows); reviews=all(x["negative_knowledge_reviewed"] and x["risk_findings_reviewed"] for x in rows)
    accepted=role_ok and quorum and independent and all_approve and reviews
    return seal({"phase":"SAED_V4_36","approvals":sorted(rows,key=lambda x:x["approval_id"]),"quorum_met":quorum,"required_roles_present":role_ok,"independent_challenge_present":independent,"mandatory_reviews_complete":reviews,"reference_agenda_accepted":accepted,"experiment_execution_authorized":False,"production_authorized":False,"research_only":True},"v436_review","review_id","review_hash")

def governance_ledger(events:list[dict],review:dict)->dict:
    rows=[]
    for x in require_list(events,"governance_events",4):
        require_exact(x,["event_type","subject_id","decision","principal_id","known_time","synthetic_fixture"]); rows.append(deepcopy(x))
    rows.append({"event_type":"AGENDA_REVIEW","subject_id":review["review_id"],"decision":"ACCEPT_REFERENCE" if review["reference_agenda_accepted"] else "REJECT","principal_id":"committee","known_time":"2026-07-17T00:00:00Z","synthetic_fixture":True})
    chain=hash_chain(sorted(rows,key=lambda x:(x["known_time"],x["event_type"],x["subject_id"])),"v436_governance")
    return seal({"phase":"SAED_V4_36","events":chain,"event_count":len(chain),"chain_head":chain[-1]["event_hash"],"append_only":True,"research_only":True},"v436_govledger","ledger_id","ledger_hash")
