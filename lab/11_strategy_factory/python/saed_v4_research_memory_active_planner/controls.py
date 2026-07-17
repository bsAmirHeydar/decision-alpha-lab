from __future__ import annotations
from copy import deepcopy
from .canonical import seal
from .contracts import require_exact,require_list,require_unique,require_num
from .errors import PlannerError

def freeze_risk_findings(items:list[dict])->dict:
    items=require_list(items,"risk_findings",4); require_unique(items,"finding_id","risk_findings"); out=[]
    for x in items:
        require_exact(x,["finding_id","candidate_id","category","severity","residual_risk","blocking","source_phase","mitigation","synthetic_fixture"]); require_num(x["residual_risk"],"residual_risk",0,1)
        if x["severity"] not in ["LOW","MEDIUM","HIGH","CRITICAL"]: raise PlannerError("risk severity invalid")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_36","records":sorted(out,key=lambda x:x["finding_id"]),"blocking_count":sum(x["blocking"] for x in out),"research_only":True},"v436_risks","register_id","register_hash")

def baseline_preservation()->dict:
    return seal({"phase":"SAED_V4_36","existing_research_results_immutable":True,"negative_results_preserved":True,"ucee_runtime_unchanged":True,"treatment_universe_unchanged":True,"portfolio_state_unchanged":True,"live_runtime_unchanged":True,"orders_submitted":0,"automatic_experiments_started":0,"failure_action":"ABSTAIN_AND_PRESERVE_BASELINE","research_only":True},"v436_baseline","receipt_id","receipt_hash")

def external_boundary()->dict:
    return seal({"phase":"SAED_V4_36","synthetic_memory_fixture":True,"real_longitudinal_memory_migration":False,"real_embedding_service":False,"external_literature_connector":False,"real_compute_scheduler":False,"external_human_committee":False,"metaeditor_compile":False,"runtime_parity":False,"prospective_evidence":False,"production_authorization":False,"live_trading":False,"research_only":True},"v436_external","boundary_id","boundary_hash")

def limitations()->dict:
    return seal({"phase":"SAED_V4_36","limitations":["synthetic reference corpus only","lexical deterministic retrieval is not semantic embedding retrieval","planner utility weights are reference policy values","no experiment is automatically launched","no real compute scheduler or external literature connector","no prospective market or broker evidence","no production or live authority"],"claim_ceiling":"synthetic_deterministic_research_memory_and_agenda_reference_only","research_only":True},"v436_limits","limitations_id","limitations_hash")
