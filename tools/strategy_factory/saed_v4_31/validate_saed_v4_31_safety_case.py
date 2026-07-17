from __future__ import annotations
import json
from _common import AR
load=lambda n:json.loads((AR/n).read_text())
coverage=load("GOLDEN_MITIGATION_COVERAGE_MATRIX.JSON"); residual=load("GOLDEN_RESIDUAL_RISK_LEDGER.JSON"); case=load("GOLDEN_ASSURANCE_CASE_GRAPH.JSON"); trace=load("GOLDEN_EVIDENCE_TRACEABILITY_MATRIX.JSON"); cert=load("GOLDEN_FORMAL_VERIFICATION_SAFETY_CASE_CERTIFICATE.JSON")
assert coverage["all_hazards_controlled"] and residual["all_within_threshold"] and case["valid"] and case["acyclic"] and case["all_nodes_reachable"] and trace["complete"]
assert cert["accepted_for_formal_verification_safety_case_research_reference"] and cert["finite_synthetic_model_claim"] and cert["bounded_temporal_semantics_claim"]
for field in ["general_program_correctness_claim","arbitrary_python_proof_claim","arbitrary_mql5_proof_claim","external_theorem_prover_certification_claim","real_market_correctness_claim","real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"]: assert cert[field] is False,field
print("V4-31 safety-case validation passed")
