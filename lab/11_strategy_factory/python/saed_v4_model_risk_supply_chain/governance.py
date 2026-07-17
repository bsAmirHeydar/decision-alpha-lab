from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique
from .errors import GovernanceError
from .canonical import hash_chain,seal

def three_lines(assignments:list[dict])->dict:
    assignments=require_list(assignments,"assignments",6); require_unique(assignments,"assignment_id","assignments"); lines=set(); out=[]
    for a in assignments:
        require_exact(a,["assignment_id","line","role","principal_id","responsibilities","independent_from","active"])
        if a["line"] not in [1,2,3] or not a["active"] or not a["responsibilities"]: raise GovernanceError("three-lines assignment invalid")
        lines.add(a["line"]); out.append(deepcopy(a))
    if lines!={1,2,3}: raise GovernanceError("all three lines required")
    return seal({"phase":"SAED_V4_35","assignments":sorted(out,key=lambda x:(x["line"],x["assignment_id"])),"three_lines_complete":True,"research_only":True},"v435_lines","registry_id","registry_hash")

def committee_review(v:dict,scorecards:dict,license_review:dict,vulnerability_review:dict,validation:dict)->dict:
    require_exact(v,["review_id","meeting_id","cutoff_time","members","quorum_required","votes","conditions","decision","minutes_hash","research_only"])
    if len(v["members"])<5 or len(v["votes"])<v["quorum_required"] or v["research_only"] is not True: raise GovernanceError("committee quorum invalid")
    blockers=any(x["blocking"] for x in scorecards["scorecards"]) or license_review["blocked"] or vulnerability_review["blocked"] or not validation["all_passed"]
    expected="REJECT_REFERENCE_RELEASE" if blockers else "ACCEPT_REFERENCE_ONLY"
    if v["decision"]!=expected: raise GovernanceError("committee decision inconsistent with blockers")
    return seal(deepcopy(v)|{"phase":"SAED_V4_35","blocking_findings_present":blockers,"production_authorized":False},"v435_committee","receipt_id","receipt_hash")

def independent_audit(v:dict,three_lines_registry:dict)->dict:
    require_exact(v,["audit_id","auditor_id","auditor_line","scope","sample_size","findings","opinion","evidence_hash","independent","synthetic_fixture"])
    if v["auditor_line"]!=3 or not v["independent"] or v["sample_size"]<10 or v["opinion"] not in ["UNQUALIFIED_REFERENCE","QUALIFIED_REFERENCE","ADVERSE"]: raise GovernanceError("independent audit invalid")
    return seal(deepcopy(v)|{"phase":"SAED_V4_35","external_audit":False,"research_only":True},"v435_audit","receipt_id","receipt_hash")

def governance_ledger(events:list[dict])->dict:
    events=require_list(events,"governance_events",8); chain=hash_chain(sorted(deepcopy(events),key=lambda x:(x["event_time"],x["event_type"],x["subject_id"])),"v435_gov_event")
    return seal({"phase":"SAED_V4_35","events":chain,"event_count":len(chain),"append_only":True,"research_only":True},"v435_govledger","ledger_id","ledger_hash")

def ucee_compatibility()->dict:
    return seal({"phase":"SAED_V4_35","ucee_schema_mutation":False,"ucee_runtime_mutation":False,"treatment_universe_mutation":False,"risk_authority_granted":False,"execution_authority_granted":False,"compatibility":"ADDITIVE_ONLY","research_only":True},"v435_ucee","review_id","review_hash")
