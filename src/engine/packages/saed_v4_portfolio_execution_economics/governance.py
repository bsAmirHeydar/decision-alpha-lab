from __future__ import annotations
from copy import deepcopy
from .canonical import seal,content_hash,merkle_root
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import GovernanceError,AuthorityError

ROLES={"PORTFOLIO_RESEARCH","EXECUTION_RESEARCH","MODEL_RISK","INDEPENDENT_CHALLENGE","OPERATIONS_OBSERVER"}

def freeze_reviews(items:list[dict],plan_hash:str)->dict:
    items=require_list(items,"reviews",5); require_unique(items,"review_id","reviews"); roles=set(); out=[]
    for x in items:
        require_exact(x,["review_id","role","reviewer_id","plan_hash","decision","findings","independent","synthetic_fixture"]); require_enum(x["role"],ROLES,"role"); require_enum(x["decision"],{"APPROVE_REFERENCE","REJECT","ABSTAIN"},"decision")
        if x["plan_hash"]!=plan_hash: raise GovernanceError("review is not plan-hash-bound")
        roles.add(x["role"]); out.append(deepcopy(x))
    required={"PORTFOLIO_RESEARCH","EXECUTION_RESEARCH","MODEL_RISK","INDEPENDENT_CHALLENGE"}
    if not required.issubset(roles): raise GovernanceError("required review roles missing")
    approved=all(x["decision"]=="APPROVE_REFERENCE" for x in out) and any(x["independent"] for x in out)
    return seal({"phase":"SAED_V4_37","reviews":sorted(out,key=lambda x:x["review_id"]),"approved_reference":approved,"capital_activation_approved":False,"production_authorized":False,"research_only":True},"v437_reviews","review_bundle_id","review_bundle_hash")

def preserve_baseline(allocation:dict,schedule:dict)->dict:
    if schedule["order_submission_allowed"] or not schedule["all_non_executable"]: raise AuthorityError("schedule expanded authority")
    return seal({"phase":"SAED_V4_37","allocation_plan_hash":allocation["plan_hash"],"schedule_hash":schedule["schedule_hash"],"ucee_mutated":False,"treatment_policy_mutated":False,"external_capital_mutated":False,"orders_submitted":False,"runtime_compiled":False,"baseline_preserved":True,"research_only":True},"v437_baseline","receipt_id","receipt_hash")

def evidence_bundle(artifacts:dict)->dict:
    hashes=[]
    for name,obj in sorted(artifacts.items()):
        if isinstance(obj,dict): hashes.append(content_hash(obj))
    return seal({"phase":"SAED_V4_37","artifact_names":sorted(artifacts),"artifact_count":len(artifacts),"artifact_hashes":hashes,"merkle_root":merkle_root(hashes),"external_broker_evidence":False,"metaeditor_evidence":False,"production_authorized":False,"research_only":True},"v437_evidence","bundle_id","bundle_hash")

def certificate(bundle:dict,reviews:dict,stress:dict,baseline:dict)->dict:
    accepted=reviews["approved_reference"] and baseline["baseline_preserved"] and stress["all_passed"]
    return seal({"kind":"v4_37_certificate","phase":"SAED_V4_37","decision":"ACCEPT_REFERENCE" if accepted else "REJECT","evidence_bundle_hash":bundle["bundle_hash"],"review_bundle_hash":reviews["review_bundle_hash"],"stress_suite_hash":stress["suite_hash"],"baseline_receipt_hash":baseline["receipt_hash"],"next_phase":"SAED_V4_38","research_only":True,"capital_activation_allowed":False,"order_submission_allowed":False,"production_authorized":False},"v437_certificate","document_id","document_hash")

def handoff(cert:dict,allocation:dict,economics:dict,schedule:dict)->dict:
    return seal({"kind":"v4_37_handoff","phase":"SAED_V4_37","certificate_hash":cert["document_hash"],"allocation_plan_hash":allocation["plan_hash"],"economics_hash":economics["economics_hash"],"schedule_hash":schedule["schedule_hash"],"next_phase":"SAED_V4_38","permitted_inputs":["frozen_portfolio_plan","frozen_cost_and_capacity_evidence","non_executable_schedule","authority_boundary"],"transferred_authority":[],"research_only":True,"production_authorized":False},"v437_handoff","document_id","document_hash")
