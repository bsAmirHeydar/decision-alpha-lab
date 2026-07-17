from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_int
from .errors import ConstitutionError
from .canonical import content_hash,seal

def freeze_constitution(v:dict)->dict:
    require_exact(v,["constitution_id","version","clauses","research_only","known_time_required","executable_prices_required","full_cost_accounting_required","automatic_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"])
    if not all(v[k] is True for k in ["research_only","known_time_required","executable_prices_required","full_cost_accounting_required"]): raise ConstitutionError("positive constitution invariant violated")
    for k in ["automatic_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"]:
        if v[k] is not False: raise ConstitutionError(f"{k} must be false")
    clauses=require_list(v["clauses"],"clauses",24); require_unique(clauses,"clause_id","clauses"); out=[]
    for c in clauses:
        require_exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]); require_int(c["priority"],"priority",1); out.append(deepcopy(c))
    body=deepcopy(v); body["clauses"]=sorted(out,key=lambda x:(x["priority"],x["clause_id"])); body["constitution_hash"]=content_hash(body); return body

def authority_boundary()->dict:
    return seal({"phase":"SAED_V4_37","research_only":True,"may_estimate_costs":True,"may_estimate_capacity":True,"may_construct_hypothetical_portfolio":True,"may_emit_non_executable_schedule":True,"may_reserve_synthetic_capital":True,"may_send_order":False,"may_activate_capital":False,"may_mutate_ucee":False,"may_promote_model":False,"may_compile_live_runtime":False,"production_authorization":False,"live_trading_authority":False,"failure_action":"ABSTAIN_PRESERVE_BASELINE_AND_ESCALATE"},"v437_authority","boundary_id","boundary_hash")
