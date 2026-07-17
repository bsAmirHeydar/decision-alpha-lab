from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]; A=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_27"
load=lambda n: json.loads((A/n).read_text(encoding="utf-8"))
auth=load("GOLDEN_AUTHORITY_BOUNDARY.JSON"); cert=load("GOLDEN_COMPLETE_SEARCH_EXPOSURE_CERTIFICATE.JSON"); exposure=load("GOLDEN_COMPLETE_EXPOSURE_LEDGER.JSON"); replay=load("GOLDEN_REPLAY_RECEIPT.JSON"); security=load("SECURITY_REVIEW.JSON")
assert auth["research_only"] and not any(auth["authority"].values())
for field in ("real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","online_fdr_claim","hidden_evaluation_air_gap_claim"): assert cert[field] is False,field
for field in ("hidden_evaluation_queries","protected_evidence_exposures","runtime_compilations","order_submissions","online_policy_mutations","network_requests"): assert exposure[field]==0,field
for field in ("hidden_evaluation_queries","protected_evidence_queries","runtime_compilations","order_submissions","online_policy_mutations"): assert replay[field]==0,field
assert replay["network_access"] is False and security["passed"]
print("V4-27 authority and security boundaries passed")
