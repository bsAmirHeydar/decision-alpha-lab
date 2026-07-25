from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_int
from .errors import ConstitutionError
from .canonical import content_hash,seal

def freeze_constitution(v:dict)->dict:
    require_exact(v,["constitution_id","version","clauses","research_only","unsigned_artifacts_allowed","unknown_license_allowed","known_critical_vulnerability_allowed","central_engine_mutation_allowed","execution_authority_allowed"])
    if v["research_only"] is not True or any(v[k] for k in ["unsigned_artifacts_allowed","unknown_license_allowed","known_critical_vulnerability_allowed","central_engine_mutation_allowed","execution_authority_allowed"]): raise ConstitutionError("constitution authority or supply-chain boundary violated")
    clauses=require_list(v["clauses"],"clauses",16); require_unique(clauses,"clause_id","clauses"); out=[]
    for c in clauses:
        require_exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]); require_int(c["priority"],"priority",1); out.append(deepcopy(c))
    body=deepcopy(v); body["clauses"]=sorted(out,key=lambda x:(x["priority"],x["clause_id"])); body["constitution_hash"]=content_hash(body); return body

def authority_boundary()->dict:
    return seal({"phase":"SAED_V4_35","research_only":True,"may_inventory_models":True,"may_score_model_risk":True,"may_quarantine_artifacts":True,"may_issue_reference_release_eligibility":True,"may_mutate_ucee":False,"may_select_treatment":False,"may_allocate_risk":False,"may_compile_live_runtime":False,"may_send_order":False,"promotion_authority":False,"production_authorization":False,"live_trading_authority":False,"failure_action":"ABSTAIN_QUARANTINE_AND_PRESERVE_BASELINE"},"v435_authority","boundary_id","boundary_hash")
