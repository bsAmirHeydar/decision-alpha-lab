from tools.repository_paths import find_repository_root
from pathlib import Path
import json

ROOT = find_repository_root(__file__)
A = ROOT / "releases/history/strategy_factory/artifacts/saed_v4_25"
certificate = json.loads((A / "GOLDEN_CONTINUAL_META_TRANSFER_CERTIFICATE.JSON").read_text(encoding="utf-8"))
authority = json.loads((A / "GOLDEN_AUTHORITY_BOUNDARY.JSON").read_text(encoding="utf-8"))
exposure = json.loads((A / "GOLDEN_EXPOSURE_LEDGER.JSON").read_text(encoding="utf-8"))
budget = json.loads((A / "GOLDEN_BUDGET_SNAPSHOT.JSON").read_text(encoding="utf-8"))
handoff = json.loads((A / "V4_25_TO_V4_26_HANDOFF.JSON").read_text(encoding="utf-8"))
assert certificate["research_only"]
assert certificate["accepted_for_continual_meta_transfer_research"]
assert all(certificate["gates"].values())
for field in (
    "decision_authority", "promotion_authority", "runtime_executable",
    "risk_allocation_authority", "execution_authority", "production_authority",
    "online_learning_authority", "real_alpha_claim", "prospective_success_claim",
    "runtime_parity_claim",
):
    assert certificate[field] is False, field
assert not any(authority["authority"].values())
assert not any(handoff["authority"].values())
for field in (
    "hidden_evaluation_queries", "protected_evidence_exposures", "runtime_compilations",
    "order_submissions", "online_policy_mutations",
):
    assert exposure[field] == 0, field
    assert budget["counts"][field] == 0, field
assert set(handoff["forbidden_next_work"]) == {
    "promotion_authorization", "runtime_compilation", "risk_allocation",
    "order_submission", "online_policy_mutation",
}
print("V4-25 authority and exposure boundaries passed")
