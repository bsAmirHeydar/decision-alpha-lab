from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import os
import re
import runpy
import subprocess
import sys
import time

ROOT = find_repository_root(__file__)
TOOL = ROOT / "src/engine/tooling/strategy_factory/saed_v4_29"
PY_ROOT = ROOT / "src/engine/packages"
env = dict(os.environ)
env["PYTHONPATH"] = str(PY_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
started = time.time()
completed = subprocess.run(
    [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        str(ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_29_hidden_evaluation_air_gap"),
    ],
    cwd=ROOT,
    env=env,
    text=True,
    capture_output=True,
)
print(completed.stdout, end="")
print(completed.stderr, end="", file=sys.stderr)
if completed.returncode:
    raise SystemExit(completed.returncode)
match = re.search(r"(\d+) passed", completed.stdout)
assert match, "pytest pass count unavailable"
test_count = int(match.group(1))

for name in [
    "validate_saed_v4_29_contracts.py",
    "validate_saed_v4_29_obsidian.py",
    "validate_saed_v4_29_mql5_static.py",
    "check_saed_v4_29_boundaries.py",
    "reproduce_saed_v4_29_golden.py",
]:
    runpy.run_path(str(TOOL / name), run_name="__main__")

AR = ROOT / "releases/history/strategy_factory/artifacts/saed_v4_29"
SC = ROOT / "schemas/legacy/strategy_factory/saed_v4_29"
DOC = ROOT / "docs/strategy_factory_sovereign_context_intelligence_v4"
MQL = list((ROOT / "mql5/Include/DecisionAlphaLab/StrategyFactory/SAED/V4_29").glob("*.mqh"))
MQL += list((ROOT / "mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_29").glob("*.mq5"))
certificate = json.loads((AR / "GOLDEN_HIDDEN_EVALUATION_AIR_GAP_CERTIFICATE.JSON").read_text())
handoff = json.loads((AR / "V4_29_TO_V4_30_HANDOFF.JSON").read_text())
phase_notes = len(list((DOC / "62_PHASE_DELIVERIES_V4/V4_29").glob("*.md")))
atomic_notes = len(list((DOC / "63_ATOMIC_CONCEPTS_V4/V4_29").glob("*.md")))
status = {
    "phase": "SAED_V4_29",
    "title": "Hidden Evaluation Air Gap",
    "version": "1.0.0",
    "status": "accepted_reference",
    "qa_passed": True,
    "python_tests": test_count,
    "closed_schemas": len(list(SC.glob("*.SCHEMA.JSON"))),
    "closed_schema_pairs": len(list(SC.glob("*.SCHEMA.JSON"))),
    "golden_exact_artifacts": len(list(AR.glob("*.JSON"))),
    "obsidian_notes": phase_notes + atomic_notes + 1,
    "phase_delivery_notes": phase_notes,
    "atomic_notes": atomic_notes,
    "mql5_static_files": len(MQL),
    "certificate_id": certificate["certificate_id"],
    "certificate_hash": certificate["certificate_hash"],
    "handoff_id": handoff["handoff_id"],
    "handoff_hash": handoff["handoff_hash"],
    "hidden_evaluation_air_gap_reference_complete": True,
    "one_shot_evaluation_count": 1,
    "researcher_hidden_label_reads": 0,
    "raw_result_egress_count": 0,
    "query_chain_verified": True,
    "custody_chain_verified": True,
    "token_chain_verified": True,
    "transport_chain_verified": True,
    "synthetic_fixture_only": True,
    "real_hidden_dataset_claim": False,
    "external_custodian_independence": "not_claimed",
    "os_air_gap_certification": "not_claimed",
    "hsm_enforcement": "not_claimed",
    "independent_external_reproduction": "pending_external",
    "independent_replication_claim": False,
    "metaeditor_compile": "pending_local_windows",
    "runtime_parity": "not_claimed",
    "broker_qualification": "not_claimed",
    "prospective_shadow": "not_claimed",
    "promotion_authority": False,
    "runtime_executable": False,
    "risk_allocation_authority": False,
    "execution_authority": False,
    "production_authorization": False,
    "online_learning_authority": False,
    "live_trading_authority": False,
    "next_phase": "SAED_V4_30",
    "claim_ceiling": "synthetic_hidden_evaluation_air_gap_reference_only_no_real_final_dataset_independent_replication_promotion_runtime_risk_execution_or_production_authority",
}
status_path = ROOT / "releases/history/strategy_factory/program/status/SAED_V4_29.json"
status_path.parent.mkdir(parents=True, exist_ok=True)
status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
qa = {
    "phase": "SAED_V4_29",
    "version": "1.0.0",
    "passed": True,
    "python_tests": test_count,
    "closed_schema_pairs": status["closed_schema_pairs"],
    "golden_artifacts": status["golden_exact_artifacts"],
    "obsidian_notes": status["obsidian_notes"],
    "mql5_static_files": status["mql5_static_files"],
    "authority_boundary_passed": True,
    "future_suffix_invariance_passed": True,
    "one_shot_reuse_negative_test_passed": True,
    "aggregate_disclosure_negative_tests_passed": True,
    "elapsed_seconds": 0.0,
    "external_evidence": {
        "metaeditor_compile": "pending_local_windows",
        "runtime_parity": "not_claimed",
        "broker_qualification": "not_claimed",
        "independent_replication": "pending_external",
    },
}
(ROOT / "releases/history/saed/reports/SAED_V4_29_QA_REPORT.json").write_text(
    json.dumps(qa, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
runpy.run_path(str(TOOL / "validate_saed_v4_29_status.py"), run_name="__main__")
print(f"V4-29 full QA passed in {time.time() - started:.2f}s")
