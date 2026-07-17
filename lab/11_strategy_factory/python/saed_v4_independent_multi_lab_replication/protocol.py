from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list
from .errors import ContractError

def freeze_protocol(value:dict)->dict:
    require_exact(value,["phase","version","minimum_labs","required_independence_dimensions","metrics","semantic_hash_required","one_run_per_lab","metric_tolerance_policy","disagreement_policy","timing_policy","disclosure_policy","research_only"],name="replication_protocol")
    if value["phase"]!="SAED_V4_30" or value["version"]!="1.0.0" or value["research_only"] is not True: raise ContractError("protocol phase/version/research boundary")
    if value["minimum_labs"]<3: raise ContractError("minimum_labs must be >=3")
    require_list(value["required_independence_dimensions"],"required_independence_dimensions",6)
    require_list(value["metrics"],"metrics",3)
    if value["semantic_hash_required"] is not True or value["one_run_per_lab"] is not True: raise ContractError("strict replication semantics required")
    out=dict(value); out["protocol_id"]=stable_id("v430_protocol",out); out["protocol_hash"]=content_hash(out)
    return out
