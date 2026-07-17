from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_int
from .errors import ConstitutionError
from .canonical import content_hash,seal

def freeze_constitution(v:dict)->dict:
    require_exact(v,["constitution_id","version","clauses","research_only","append_only_memory","negative_results_mandatory","future_suffix_access_allowed","automatic_experiment_execution_allowed","treatment_selection_allowed","capital_allocation_allowed","production_authorization_allowed"])
    if v["research_only"] is not True or v["append_only_memory"] is not True or v["negative_results_mandatory"] is not True: raise ConstitutionError("memory constitution invariant violated")
    for k in ["future_suffix_access_allowed","automatic_experiment_execution_allowed","treatment_selection_allowed","capital_allocation_allowed","production_authorization_allowed"]:
        if v[k] is not False: raise ConstitutionError(f"{k} must be false")
    clauses=require_list(v["clauses"],"clauses",18); require_unique(clauses,"clause_id","clauses"); out=[]
    for c in clauses:
        require_exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]); require_int(c["priority"],"priority",1); out.append(deepcopy(c))
    body=deepcopy(v); body["clauses"]=sorted(out,key=lambda x:(x["priority"],x["clause_id"])); body["constitution_hash"]=content_hash(body); return body

def authority_boundary()->dict:
    return seal({"phase":"SAED_V4_36","research_only":True,"may_record_memory":True,"may_retrieve_evidence":True,"may_rank_research_proposals":True,"may_emit_human_review_agenda":True,"may_execute_experiment":False,"may_mutate_ucee":False,"may_select_treatment":False,"may_allocate_capital":False,"may_compile_live_runtime":False,"may_send_order":False,"promotion_authority":False,"production_authorization":False,"live_trading_authority":False,"failure_action":"ABSTAIN_PRESERVE_BASELINE_AND_ESCALATE"},"v436_authority","boundary_id","boundary_hash")
