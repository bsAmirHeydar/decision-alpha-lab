from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id

def build(evidence:dict[str,Any], authority:dict[str,Any])->dict[str,Any]:
    gates={
      "upstream_verified":evidence["upstream_receipt"]["hash_verified"],
      "dataset_valid":evidence["dataset_summary"]["known_time_verified"],
      "attribution_complete":evidence["attributions"]["record_count"]==evidence["dataset_summary"]["record_count"],
      "pathway_complete":len(evidence["pathways"]["records"])==evidence["dataset_summary"]["record_count"],
      "concept_controls_passed":evidence["concept_probes"]["reference_gate_passed"],
      "causal_trace_complete":len(evidence["causal_traces"]["records"])==evidence["dataset_summary"]["record_count"],
      "counterfactual_complete":len(evidence["counterfactuals"]["records"])==evidence["dataset_summary"]["record_count"],
      "dictionary_control_passed":evidence["sparse_dictionary"]["reference_gate_passed"],
      "faithfulness_passed":evidence["faithfulness"]["reference_gate_passed"],
      "sanity_passed":evidence["sanity"]["reference_gate_passed"],
      "stability_passed":evidence["stability"]["reference_gate_passed"],
      "critical_shortcuts_absent":evidence["shortcut_audit"]["critical_shortcuts_absent"],
      "critical_failures_absent":evidence["failure_catalogue"]["critical_count"]==0,
      "budget_respected":evidence["budget_snapshot"]["within_budget"],
      "exposure_zero":all(evidence["exposure_ledger"][k]==0 for k in ["hidden_evaluation_queries","protected_evidence_exposures","runtime_compilations","order_submissions","online_policy_mutations","network_requests"]),
      "authority_zero":not any(authority["authority"].values()),
      "baseline_preserved":True,
    }
    hashes={k:next((v for f,v in value.items() if f.endswith("_hash")),content_hash(value)) for k,value in sorted(evidence.items())}
    payload={"phase":"SAED_V4_26","version":"1.0.0","accepted_for_mechanistic_interpretability_research":all(gates.values()),"gates":gates,"evidence_hashes":hashes,"authority_boundary":authority,"research_only":True,"claim_class":"mechanistic_research_not_causal_proof","decision_authority":False,"promotion_authority":False,"runtime_executable":False,"risk_allocation_authority":False,"execution_authority":False,"production_authority":False,"online_learning_authority":False,"real_alpha_claim":False,"prospective_success_claim":False,"runtime_parity_claim":False}
    payload["certificate_id"]=stable_id("mechanistic_interpretability_certificate",payload); payload["certificate_hash"]=content_hash(payload)
    return payload

def handoff(certificate:dict[str,Any])->dict[str,Any]:
    payload={"phase":"SAED_V4_26","next_phase":"SAED_V4_27","certificate_id":certificate["certificate_id"],"certificate_hash":certificate["certificate_hash"],"entry_gates":{"mechanistic_certificate_verified":certificate["accepted_for_mechanistic_interpretability_research"],"trial_ledger_available":True,"exposure_ledger_available":True,"failure_catalogue_available":True,"promotion_denied":True,"runtime_denied":True,"research_only":True},"allowed_next_work":["complete_trial_registry","complete_query_registry","chart_exposure_registry","narrative_exposure_registry","agent_exposure_registry","manual_intervention_registry","failed_run_registry","search_family_freeze","exposure_deduplication"],"forbidden_next_work":["promotion_authorization","runtime_compilation","risk_allocation","order_submission","online_policy_mutation"],"research_only":True,"authority":{"decision":False,"promotion":False,"runtime":False,"risk_allocation":False,"execution":False,"production":False}}
    payload["handoff_id"]=stable_id("v4_26_to_v4_27",payload); payload["handoff_hash"]=content_hash(payload)
    return payload
