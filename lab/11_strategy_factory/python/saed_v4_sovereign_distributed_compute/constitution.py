from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_positive_int,require_sorted_unique_strings
from .errors import ConstitutionError
from .canonical import content_hash,seal

def freeze_constitution(value:dict)->dict:
    require_exact(value,["constitution_id","version","clauses","research_only","raw_data_export_allowed","public_network_egress_allowed","central_engine_mutation_allowed","execution_authority_allowed"])
    if value["research_only"] is not True or value["raw_data_export_allowed"] or value["public_network_egress_allowed"] or value["central_engine_mutation_allowed"] or value["execution_authority_allowed"]: raise ConstitutionError("constitution authority boundary violated")
    clauses=require_list(value["clauses"],"clauses",12); require_unique(clauses,"clause_id","clauses")
    out=[]
    for c in clauses:
        require_exact(c,["clause_id","priority","requirement","failure_action","evidence_required"])
        require_positive_int(c["priority"],"priority"); out.append(deepcopy(c))
    body=deepcopy(value); body["clauses"]=sorted(out,key=lambda x:(x["priority"],x["clause_id"])); body["constitution_hash"]=content_hash(body); return body

def authority_boundary()->dict:
    return seal({"phase":"SAED_V4_34","research_only":True,"may_plan_distributed_compute":True,"may_simulate_execution":True,"may_emit_evidence":True,"may_export_raw_data":False,"may_mutate_ucee":False,"may_select_treatment":False,"may_allocate_risk":False,"may_compile_live_runtime":False,"may_send_order":False,"promotion_authority":False,"production_authorization":False,"live_trading_authority":False,"failure_action":"ABSTAIN_AND_PRESERVE_BASELINE"},"v434_authority","boundary_id","boundary_hash")
