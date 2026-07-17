from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
INDEX = ROOT / "SAED_V4_26_FILE_INDEX.txt"
LEDGER = ROOT / "SAED_V4_26_FILE_HASHES.sha256"
MANIFEST = ROOT / "SAED_V4_26_PATCH_MANIFEST.json"
QA = ROOT / "SAED_V4_26_QA_REPORT.json"
INVENTORY = ROOT / "SAED_V4_26_ARTIFACT_INVENTORY.csv"
assert all(path.is_file() for path in [INDEX, LEDGER, MANIFEST, QA, INVENTORY])

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
assert set(expected) == set(paths) - {"SAED_V4_26_FILE_HASHES.sha256"}
for path, digest in expected.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
qa = json.loads(QA.read_text(encoding="utf-8"))
status = json.loads((ROOT / "lab/11_strategy_factory/phase_status/SAED_V4_26.json").read_text(encoding="utf-8"))
assert manifest["phase"] == "SAED_V4_26" and manifest["version"] == "1.0.0"
assert manifest["file_count"] == len(paths) and manifest["hash_count"] == len(expected)
assert manifest["qa_passed"] and qa["passed"] and status["qa_passed"]
assert status["python_tests"] == 121 and status["closed_schemas"] == 39
assert status["obsidian_notes"] == 323 and status["mql5_static_files"] == 25
assert status["metaeditor_compile"] == "pending_local_windows"
for field in ("real_alpha", "promotion_authority", "runtime_executable", "risk_allocation_authority", "execution_authority", "production_authorization", "online_learning_authority"):
    assert status[field] is False, field

A = ROOT / "lab/11_strategy_factory/artifacts/saed_v4_26"
certificate = json.loads((A / "GOLDEN_MECHANISTIC_INTERPRETABILITY_CERTIFICATE.JSON").read_text(encoding="utf-8"))
assert certificate["accepted_for_mechanistic_interpretability_research"]
assert all(certificate["gates"].values()) and certificate["research_only"]
for field in ("decision_authority", "promotion_authority", "runtime_executable", "risk_allocation_authority", "execution_authority", "production_authority", "online_learning_authority", "real_alpha_claim", "prospective_success_claim", "runtime_parity_claim"):
    assert certificate[field] is False, field

handoff = json.loads((A / "V4_26_TO_V4_27_HANDOFF.JSON").read_text(encoding="utf-8"))
assert handoff["next_phase"] == "SAED_V4_27" and all(handoff["entry_gates"].values())
assert handoff["research_only"] and not any(handoff["authority"].values())
assert set(handoff["allowed_next_work"]) == {"complete_trial_registry", "complete_query_registry", "chart_exposure_registry", "narrative_exposure_registry", "agent_exposure_registry", "manual_intervention_registry", "failed_run_registry", "search_family_freeze", "exposure_deduplication"}

budget = json.loads((A / "GOLDEN_BUDGET_SNAPSHOT.JSON").read_text(encoding="utf-8"))
assert budget["complete"] and budget["within_budget"]
assert budget["counts"] == {"concept_probes": 240, "counterfactual_trials": 1920, "dictionary_trials": 3, "feature_ablations": 240, "hidden_evaluation_queries": 0, "online_policy_mutations": 0, "order_submissions": 0, "patch_interventions": 36, "pathway_ablations": 200, "protected_evidence_exposures": 0, "records": 40, "runtime_compilations": 0, "trace_interventions": 280}

exposure = json.loads((A / "GOLDEN_EXPOSURE_LEDGER.JSON").read_text(encoding="utf-8"))
for field in ("hidden_evaluation_queries", "protected_evidence_exposures", "runtime_compilations", "order_submissions", "online_policy_mutations", "network_requests"):
    assert exposure[field] == 0, field
assert exposure["complete_for_v4_26"] and exposure["v4_27_complete_exposure_ledger_not_claimed"]

faith = json.loads((A / "GOLDEN_FAITHFULNESS_REPORT.JSON").read_text(encoding="utf-8"))
sanity = json.loads((A / "GOLDEN_SANITY_CHECK_REPORT.JSON").read_text(encoding="utf-8"))
stability = json.loads((A / "GOLDEN_MECHANISM_STABILITY_REPORT.JSON").read_text(encoding="utf-8"))
shortcuts = json.loads((A / "GOLDEN_SHORTCUT_AUDIT.JSON").read_text(encoding="utf-8"))
failures = json.loads((A / "GOLDEN_MECHANISTIC_FAILURE_CATALOGUE.JSON").read_text(encoding="utf-8"))
assert faith["reference_gate_passed"] and sanity["reference_gate_passed"] and stability["reference_gate_passed"]
assert shortcuts["critical_shortcuts_absent"] and failures["critical_count"] == 0

replay = json.loads((A / "GOLDEN_REPLAY_RECEIPT.JSON").read_text(encoding="utf-8"))
assert replay["deterministic"] and replay["network_access"] is False
for field in ("future_suffix_queries", "protected_evidence_queries", "hidden_evaluation_queries", "runtime_compilations", "order_submissions", "online_policy_mutations"):
    assert replay[field] == 0, field

with INVENTORY.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == len(paths)
assert {row["path"] for row in rows} == set(paths)
print(f"V4-26 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
