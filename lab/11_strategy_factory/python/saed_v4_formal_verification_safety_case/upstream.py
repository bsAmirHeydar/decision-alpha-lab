from __future__ import annotations
from .contracts import require_exact,require_bool_false,require_sha256
from .canonical import content_hash,stable_id
from .errors import ContractError

def verify_upstream(documents:dict)->dict:
    require_exact(documents,["certificate","handoff"],name="upstream_documents")
    certificate=documents["certificate"]; handoff=documents["handoff"]
    require_exact(certificate,["phase","certificate_id","certificate_hash","accepted_for_independent_multi_lab_replication_research_reference","research_only","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"],name="v430_certificate_projection")
    require_exact(handoff,["phase","next_phase","handoff_id","handoff_hash","certificate_id","certificate_hash","entry_gates","allowed_next_work","forbidden_next_work","authority","research_only"],name="v430_handoff_projection")
    if certificate["phase"]!="SAED_V4_30" or handoff["phase"]!="SAED_V4_30" or handoff["next_phase"]!="SAED_V4_31": raise ContractError("wrong upstream phase")
    if not certificate["accepted_for_independent_multi_lab_replication_research_reference"] or not certificate["research_only"] or not handoff["research_only"]: raise ContractError("upstream not accepted research reference")
    for key in ["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"]: require_bool_false(certificate[key],key)
    if any(handoff["authority"].values()): raise ContractError("upstream authority must be zero")
    require_sha256(certificate["certificate_hash"],"certificate_hash"); require_sha256(handoff["handoff_hash"],"handoff_hash")
    required={"formal_invariant_catalog","safety_property_specification","model_checking_reference","proof_obligation_registry","assurance_case_graph","hazard_and_mitigation_ledger"}
    if not required.issubset(set(handoff["allowed_next_work"])): raise ContractError("upstream does not authorize required work")
    body={"phase":"SAED_V4_31","upstream_phase":"SAED_V4_30","certificate_id":certificate["certificate_id"],"certificate_hash":certificate["certificate_hash"],"handoff_id":handoff["handoff_id"],"handoff_hash":handoff["handoff_hash"],"allowed_work_verified":True,"authority_zero":True,"verified":True,"research_only":True}
    body["receipt_id"]=stable_id("v431_upstream_receipt",body); body["receipt_hash"]=content_hash(body); return body
