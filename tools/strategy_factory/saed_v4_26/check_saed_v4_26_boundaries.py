from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]; A=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_26"; load=lambda n:json.loads((A/n).read_text())
c=load("GOLDEN_MECHANISTIC_INTERPRETABILITY_CERTIFICATE.JSON"); a=load("GOLDEN_AUTHORITY_BOUNDARY.JSON"); e=load("GOLDEN_EXPOSURE_LEDGER.JSON"); h=load("V4_26_TO_V4_27_HANDOFF.JSON")
assert c["accepted_for_mechanistic_interpretability_research"] and all(c["gates"].values()) and c["research_only"]
for f in ["decision_authority","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","real_alpha_claim","prospective_success_claim","runtime_parity_claim"]: assert c[f] is False
assert not any(a["authority"].values()) and not any(h["authority"].values())
for f in ["hidden_evaluation_queries","protected_evidence_exposures","runtime_compilations","order_submissions","online_policy_mutations","network_requests"]: assert e[f]==0
assert set(h["forbidden_next_work"])=={"promotion_authorization","runtime_compilation","risk_allocation","order_submission","online_policy_mutation"}
print("V4-26 authority and exposure boundaries passed")
