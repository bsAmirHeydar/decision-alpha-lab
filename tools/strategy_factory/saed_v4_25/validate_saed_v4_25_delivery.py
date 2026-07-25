from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
INDEX = ROOT / "releases/history/saed/indexes/SAED_V4_25_FILE_INDEX.txt"
LEDGER = ROOT / "releases/history/saed/hashes/SAED_V4_25_FILE_HASHES.sha256"
MANIFEST = ROOT / "releases/history/saed/manifests/SAED_V4_25_PATCH_MANIFEST.json"
QA = ROOT / "releases/history/saed/reports/SAED_V4_25_QA_REPORT.json"
INVENTORY = ROOT / "releases/history/saed/inventories/SAED_V4_25_ARTIFACT_INVENTORY.csv"
required = [INDEX, LEDGER, MANIFEST, QA, INVENTORY]
assert all(path.is_file() for path in required)

paths = [line.strip() for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
assert paths == sorted(paths)
assert len(paths) == len(set(paths))
assert not [path for path in paths if not (ROOT / path).is_file()]
assert not [path for path in paths if "__pycache__" in path or path.endswith(".pyc")]

expected = {}
for line in LEDGER.read_text(encoding="utf-8").splitlines():
    if line.strip():
        digest, path = line.split("  ", 1)
        expected[path] = digest
assert set(expected) == set(paths) - {"releases/history/saed/hashes/SAED_V4_25_FILE_HASHES.sha256"}
for path, digest in expected.items():
    actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    assert actual == digest, path

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
qa = json.loads(QA.read_text(encoding="utf-8"))
status = json.loads((ROOT / "lab/11_strategy_factory/phase_status/SAED_V4_25.json").read_text(encoding="utf-8"))
assert manifest["phase"] == "SAED_V4_25" and manifest["version"] == "1.0.0"
assert manifest["file_count"] == len(paths) and manifest["hash_count"] == len(expected)
assert manifest["qa_passed"] and qa["passed"] and status["qa_passed"]
assert status["python_tests"] == 170 and status["closed_schemas"] == 36
assert status["obsidian_notes"] == 255 and status["mql5_static_files"] == 22
assert status["metaeditor_compile"] == "pending_local_windows"
assert status["real_alpha"] is False and status["promotion_authority"] is False
assert status["runtime_executable"] is False and status["risk_allocation_authority"] is False
assert status["execution_authority"] is False and status["production_authorization"] is False
assert status["online_learning_authority"] is False

A = ROOT / "lab/11_strategy_factory/artifacts/saed_v4_25"
certificate = json.loads((A / "GOLDEN_CONTINUAL_META_TRANSFER_CERTIFICATE.JSON").read_text(encoding="utf-8"))
assert certificate["accepted_for_continual_meta_transfer_research"]
assert all(certificate["gates"].values())
assert certificate["research_only"]
assert certificate["guard_fallback_count"] >= 1
for field in (
    "decision_authority", "promotion_authority", "runtime_executable",
    "risk_allocation_authority", "execution_authority", "production_authority",
    "online_learning_authority", "real_alpha_claim", "prospective_success_claim",
    "runtime_parity_claim",
):
    assert certificate[field] is False, field

handoff = json.loads((A / "V4_25_TO_V4_26_HANDOFF.JSON").read_text(encoding="utf-8"))
assert handoff["next_phase"] == "SAED_V4_26"
assert all(handoff["entry_gates"].values())
assert handoff["research_only"] and not any(handoff["authority"].values())
assert set(handoff["allowed_next_work"]) == {
    "frozen_feature_attribution", "transfer_pathway_attribution",
    "adaptation_parameter_mechanism_analysis", "continual_calibration_component_analysis",
    "counterfactual_mechanism_probes", "mechanistic_failure_catalogue",
}

exposure = json.loads((A / "GOLDEN_EXPOSURE_LEDGER.JSON").read_text(encoding="utf-8"))
assert exposure["complete"]
for field in (
    "hidden_evaluation_queries", "protected_evidence_exposures", "runtime_compilations",
    "order_submissions", "online_policy_mutations", "network_requests",
):
    assert exposure[field] == 0, field

budget = json.loads((A / "GOLDEN_BUDGET_SNAPSHOT.JSON").read_text(encoding="utf-8"))
assert budget["complete"] and budget["within_budget"]
assert budget["counts"]["tasks"] == 48
assert budget["counts"]["source_evaluations"] == 576
assert budget["counts"]["adaptations"] == 48
assert budget["counts"]["replay_entries"] == 12
assert budget["counts"]["recalibration_trials"] == 27
assert budget["counts"]["bootstrap_draws"] == 400

transfer = json.loads((A / "GOLDEN_TRANSFER_REPORT.JSON").read_text(encoding="utf-8"))
assert transfer["accepted_for_transfer_research"]
assert all(transfer["gates"].values())
assert transfer["forward_transfer_ci_lower"] >= -0.01
assert transfer["mean_forgetting"] <= 0.04

leakage = json.loads((A / "KNOWN_TIME_LEAKAGE_REVIEW.JSON").read_text(encoding="utf-8"))
assert leakage["passed"]
assert leakage["decision_artifacts_use_query_outcomes"] is False
assert leakage["adaptation_uses_query_outcomes"] is False
assert leakage["future_source_queries"] == 0
assert leakage["future_suffix_queries"] == 0
assert leakage["protected_evidence_queries"] == 0

replay = json.loads((A / "GOLDEN_REPLAY_RECEIPT.JSON").read_text(encoding="utf-8"))
assert replay["deterministic"] and replay["network_access"] is False
assert replay["future_suffix_queries"] == 0 and replay["protected_evidence_queries"] == 0
assert replay["runtime_compilations"] == 0 and replay["order_submissions"] == 0
assert replay["online_policy_mutations"] == 0

with INVENTORY.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == len(paths)
assert {row["path"] for row in rows} == set(paths)
print(f"V4-25 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
