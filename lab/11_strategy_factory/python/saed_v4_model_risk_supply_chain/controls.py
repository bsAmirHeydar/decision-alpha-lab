from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_time_before
from .errors import GovernanceError
from .canonical import seal

def exception_register(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"exceptions",1); require_unique(items,"exception_id","exceptions"); out=[]
    for x in items:
        require_exact(x,["exception_id","subject_id","control_id","rationale","compensating_controls","owner_id","approver_ids","issued_time","expires_time","status","production_scope_allowed","synthetic_fixture"])
        require_time_before(x["issued_time"],cutoff,"exception issued_time")
        if x["status"]!="REFERENCE_ONLY" or x["production_scope_allowed"] or len(x["approver_ids"])<2 or not x["compensating_controls"]: raise GovernanceError("exception invalid")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_35","exceptions":sorted(out,key=lambda x:x["exception_id"]),"auto_expiry_required":True,"production_waivers":False,"research_only":True},"v435_exceptions","registry_id","registry_hash")

def waiver_review(exceptions:dict,cutoff:str)->dict:
    rows=[]; active=0
    for x in exceptions["exceptions"]:
        expired=x["expires_time"]<=cutoff; state="EXPIRED" if expired else "ACTIVE_REFERENCE"; active+=0 if expired else 1
        rows.append({"exception_id":x["exception_id"],"state":state,"production_scope_allowed":False,"revalidation_required":not expired})
    return seal({"phase":"SAED_V4_35","reviews":rows,"active_reference_waivers":active,"expired_waivers":len(rows)-active,"research_only":True},"v435_waivers","review_id","review_hash")

def quarantine(license_review:dict,vulnerability_review:dict,scorecards:dict)->dict:
    items=[]
    for r in license_review["reviews"]:
        if r["decision"]=="QUARANTINE":items.append({"subject_id":r["component_id"],"reason":"LICENSE","source_id":license_review["review_id"],"state":"QUARANTINED"})
    for r in vulnerability_review["findings"]:
        if r["decision"]=="QUARANTINE":items.append({"subject_id":r["component_id"],"reason":"VULNERABILITY","source_id":vulnerability_review["review_id"],"state":"QUARANTINED"})
    for r in scorecards["scorecards"]:
        if r["blocking"]:items.append({"subject_id":r["model_id"],"reason":"MODEL_RISK","source_id":scorecards["registry_id"],"state":"QUARANTINED"})
    # exact dedup
    unique={(x["subject_id"],x["reason"]):x for x in items}
    return seal({"phase":"SAED_V4_35","items":[unique[k] for k in sorted(unique)],"item_count":len(unique),"fail_closed":True,"baseline_preserved":True,"research_only":True},"v435_quarantine","registry_id","registry_hash")

def incident_plan(v:dict)->dict:
    require_exact(v,["plan_id","severity_levels","triggers","roles","containment_actions","evidence_preservation","notification_matrix","recovery_gates","tabletop_completed","research_only"])
    for k,m in [("severity_levels",4),("triggers",8),("roles",5),("containment_actions",8),("notification_matrix",4),("recovery_gates",6)]:require_list(v[k],k,m)
    if not v["evidence_preservation"] or not v["tabletop_completed"] or not v["research_only"]:raise GovernanceError("incident plan incomplete")
    return seal(deepcopy(v)|{"phase":"SAED_V4_35"},"v435_incident","receipt_id","receipt_hash")

def recall_plan(v:dict)->dict:
    require_exact(v,["plan_id","recall_levels","artifact_graph_required","kill_distribution_required","consumer_notification_required","revocation_required","rollback_required","drill_completed","research_only"])
    if not all(v[k] for k in ["artifact_graph_required","kill_distribution_required","consumer_notification_required","revocation_required","rollback_required","drill_completed","research_only"]):raise GovernanceError("recall plan incomplete")
    return seal(deepcopy(v)|{"phase":"SAED_V4_35"},"v435_recall","receipt_id","receipt_hash")
