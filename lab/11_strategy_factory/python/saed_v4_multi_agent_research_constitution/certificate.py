from __future__ import annotations
from .canonical import content_hash,stable_id

def build_evidence_bundle(evidence:dict)->dict:
    ids={}; hashes={}
    for key,value in evidence.items():
        if not isinstance(value,dict): continue
        ids[key]=next((v for k,v in value.items() if k.endswith("_id")),"")
        hashes[key]=content_hash(value)
    body={"phase":"SAED_V4_32","evidence_ids":ids,"evidence_hashes":hashes,"complete":True,"synthetic_fixture_only":True,"external_agent_execution":False,"research_only":True}
    body["bundle_id"]=stable_id("v432_evidence_bundle",body); body["bundle_hash"]=content_hash(body); return body

def build_certificate(e:dict)->dict:
    gates={
      "upstream_verified":e["upstream"]["entry_gate_passed"],
      "constitution_closed":e["constitution"]["closed_contract"],
      "role_registry_complete":len(e["roles"]["roles"])>=10,
      "deny_by_default":e["capabilities"]["deny_by_default"],
      "separation_of_duties":e["separation"]["self_approval_denied"],
      "task_graph_acyclic":e["tasks"]["acyclic"],
      "deterministic_schedule":e["plan"]["deterministic"],
      "memory_isolation":e["memory"]["cross_agent_write_denied"],
      "source_attribution_complete":e["attribution"]["all_claims_attributed"],
      "dissent_preserved":e["contradictions"]["dissent_preserved"],
      "exposure_accounting_complete":e["exposure"]["complete"],
      "budgets_within_limit":e["budget_ledger"]["all_within_budget"],
      "human_review_present":e["checkpoints"]["human_review_present"],
      "quorum_valid":e["quorum"]["all_quorums_met"],
      "authority_zero":all(v is False for v in e["authority"]["authority"].values()),
      "replay_exact":e["replay"]["deterministic"],
      "independent_reproduction_exact":e["reproduction"]["exact_match"],
      "security_review_passed":e["security"]["passed"],
      "known_time_review_passed":e["known_time"]["passed"],
      "contract_closure_passed":e["contract_closure"]["passed"]
    }
    body={"phase":"SAED_V4_32","title":"Multi Agent Research Constitution","version":"1.0.0","claim_class":"closed_contract_multi_agent_research_governance_reference_implementation","gates":gates,"all_gates_passed":all(gates.values()),"accepted_reference":all(gates.values()),"synthetic_fixture_only":True,"external_agent_runtime_claim":False,"agent_collusion_absence_claim":False,"promotion_authority":False,"runtime_authority":False,"risk_allocation_authority":False,"execution_authority":False,"production_authorization":False,"online_learning_authority":False,"live_trading_authority":False,"research_only":True,"authority_boundary":e["authority"],"evidence_bundle_id":e["evidence_bundle"]["bundle_id"],"evidence_bundle_hash":e["evidence_bundle"]["bundle_hash"],"claim_ceiling":e["limitations"]["claim_ceiling"]}
    body["certificate_id"]=stable_id("v432_multi_agent_constitution_certificate",body); body["certificate_hash"]=content_hash(body); return body

def handoff(certificate:dict)->dict:
    body={"phase":"SAED_V4_32","next_phase":"SAED_V4_33","certificate_id":certificate["certificate_id"],"certificate_hash":certificate["certificate_hash"],"entry_gates":{"multi_agent_constitution_accepted":certificate["accepted_reference"],"authority_zero":certificate["gates"]["authority_zero"],"research_only":True,"source_attribution_complete":certificate["gates"]["source_attribution_complete"],"human_review_present":certificate["gates"]["human_review_present"]},"allowed_next_work":["federated_research_contracts","confidential_aggregation_reference","privacy_budget_accounting","cross_cell_identity_attestation","secure_update_envelopes","federated_provenance","federated_adversarial_review"],"forbidden_next_work":["grant_agent_promotion_authority","grant_agent_trading_authority","unreviewed_constitution_amendment","protected_evidence_broadcast","live_credential_distribution","runtime_activation","risk_allocation","order_submission","production_release"],"authority":{"promotion":False,"runtime":False,"risk_allocation":False,"execution":False,"production":False,"online_learning":False,"live_trading":False},"research_only":True}
    body["handoff_id"]=stable_id("v4_32_to_v4_33",body); body["handoff_hash"]=content_hash(body); return body
