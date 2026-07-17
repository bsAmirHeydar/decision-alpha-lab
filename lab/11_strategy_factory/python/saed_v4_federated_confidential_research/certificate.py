from __future__ import annotations
from .canonical import content_hash,seal

def evidence_bundle(e:dict):
    refs=[]
    for key in sorted(e):
        obj=e[key]
        if isinstance(obj,dict): refs.append({"artifact":key,"content_hash":content_hash(obj)})
    return seal({"phase":"SAED_V4_33","artifact_refs":refs,"artifact_count":len(refs),"synthetic_fixture_only":True,"research_only":True},"v433_evidence_bundle","bundle_id","bundle_hash")

def certificate(e:dict):
    gates={
      "upstream_verified":e["upstream"]["verified"],"constitution_frozen":bool(e["constitution"]["constitution_hash"]),"cells_attested":e["attestations"]["all_cells_attested"],"raw_data_local":e["residency"]["all_raw_data_local"],"eligibility_threshold":e["eligibility"]["threshold_met"],"privacy_budget_respected":e["privacy_budget"]["budget_respected"],"aggregation_threshold":e["aggregation_transcript"]["participant_threshold_met"],"raw_vectors_not_disclosed":not e["aggregation_transcript"]["raw_individual_vectors_disclosed"],"provenance_complete":e["provenance"]["complete"],"exposure_complete":e["exposure"]["complete"],"human_review":e["human_reviews"]["all_approved"],"adversarial_review":e["adversarial_review"]["all_passed"],"incidents_contained":e["incidents"]["all_contained"],"deterministic_replay":e["replay"]["deterministic"],"zero_authority":e["authority"]["all_zero"]}
    body={"phase":"SAED_V4_33","title":"Federated Confidential Research","version":"1.0.0","gates":gates,"all_gates_passed":all(gates.values()),"accepted_reference":all(gates.values()),"synthetic_fixture_only":True,"real_federated_runtime_claim":False,"real_confidentiality_claim":False,"formal_privacy_guarantee_claim":False,"promotion_authority":False,"runtime_authority":False,"risk_allocation_authority":False,"execution_authority":False,"production_authority":False,"research_only":True,"claim_ceiling":"deterministic_closed_contract_federated_confidential_research_reference_only_no_real_crypto_network_privacy_promotion_runtime_risk_execution_or_production_authority"}
    return seal(body,"v433_federated_certificate","certificate_id","certificate_hash")

def handoff(cert:dict):
    body={"phase":"SAED_V4_33","next_phase":"SAED_V4_34","certificate_id":cert["certificate_id"],"certificate_hash":cert["certificate_hash"],"entry_gates":{"federated_reference_accepted":cert["accepted_reference"],"zero_authority":cert["gates"]["zero_authority"],"raw_data_local":cert["gates"]["raw_data_local"],"privacy_budget_respected":cert["gates"]["privacy_budget_respected"],"research_only":True},"allowed_next_work":["sovereign_worker_registry","deterministic_job_dag","resource_quota_enforcement","artifact_locality_scheduler","sealed_execution_receipts","distributed_replay","failure_recovery_reference"],"forbidden_next_work":["live_credential_distribution","raw_data_export","unreviewed_remote_execution","runtime_activation","risk_allocation","order_submission","production_release"],"authority":{"promotion":False,"runtime":False,"risk_allocation":False,"execution":False,"production":False,"online_learning":False,"live_trading":False},"research_only":True}
    return seal(body,"v4_33_to_v4_34","handoff_id","handoff_hash")
