from __future__ import annotations
import json
import os
import re
import runpy
import subprocess
import sys
import time
from _common import ROOT, AR, SC, DOC, PY_ROOT, MQL_INCLUDE, MQL_EXPERT

started = time.perf_counter()
tool = ROOT / "src/engine/tooling/strategy_factory/saed_v4_32"
env = dict(os.environ)
env["PYTHONPATH"] = str(PY_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
completed = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", str(ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_32_multi_agent_research_constitution")],
    cwd=ROOT, env=env, text=True, capture_output=True
)
print(completed.stdout, end="")
print(completed.stderr, end="", file=sys.stderr)
if completed.returncode:
    raise SystemExit(completed.returncode)
match = re.search(r"(\d+) passed", completed.stdout)
assert match
python_tests = int(match.group(1))

for name in [
    "validate_saed_v4_32_contracts.py",
    "validate_saed_v4_32_governance.py",
    "check_saed_v4_32_boundaries.py",
    "validate_saed_v4_32_replay.py",
    "validate_saed_v4_32_obsidian.py",
    "validate_saed_v4_32_mql5_static.py",
]:
    runpy.run_path(str(tool / name), run_name="__main__")

certificate = json.loads((AR / "GOLDEN_MULTI_AGENT_RESEARCH_CONSTITUTION_CERTIFICATE.JSON").read_text(encoding="utf-8"))
handoff = json.loads((AR / "V4_32_TO_V4_33_HANDOFF.JSON").read_text(encoding="utf-8"))
phase_notes = len(list((DOC / "62_PHASE_DELIVERIES_V4/V4_32").glob("*.md")))
atomic_notes = len(list((DOC / "63_ATOMIC_CONCEPTS_V4/V4_32").glob("*.md")))
obsidian_notes = phase_notes + atomic_notes + 1
mql5_files = len(list(MQL_INCLUDE.glob("*.mqh"))) + len(list(MQL_EXPERT.glob("*.mq5")))
elapsed = round(time.perf_counter() - started, 6)

status = {
    "phase": "SAED_V4_32",
    "title": "Multi Agent Research Constitution",
    "version": "1.0.0",
    "status": "accepted_reference",
    "qa_passed": True,
    "python_tests": python_tests,
    "closed_schemas": len(list(SC.glob("*.SCHEMA.JSON"))),
    "closed_schema_pairs": len(list(SC.glob("*.SCHEMA.JSON"))),
    "golden_exact_artifacts": len(list(AR.glob("*.JSON"))),
    "obsidian_notes": obsidian_notes,
    "phase_delivery_notes": phase_notes,
    "atomic_notes": atomic_notes,
    "mql5_static_files": mql5_files,
    "certificate_id": certificate["certificate_id"],
    "certificate_hash": certificate["certificate_hash"],
    "handoff_id": handoff["handoff_id"],
    "handoff_hash": handoff["handoff_hash"],
    "deny_by_default_verified": True,
    "zero_live_authority_verified": True,
    "self_approval_denied": True,
    "memory_isolation_verified": True,
    "complete_exposure_accounting": True,
    "claim_source_attribution_complete": True,
    "dissent_preserved": True,
    "human_review_quorum_verified": True,
    "hard_budget_enforcement_verified": True,
    "incident_containment_verified": True,
    "synthetic_fixture_only": True,
    "external_agent_runtime": "not_claimed",
    "real_agent_collusion_resistance": "not_claimed",
    "metaeditor_compile": "pending_local_windows",
    "runtime_parity": "not_claimed",
    "broker_qualification": "not_claimed",
    "prospective_shadow": "not_claimed",
    "real_alpha": "not_claimed",
    "promotion_authority": False,
    "runtime_executable": False,
    "risk_allocation_authority": False,
    "execution_authority": False,
    "production_authorization": False,
    "online_learning_authority": False,
    "live_trading_authority": False,
    "next_phase": "SAED_V4_33",
    "claim_ceiling": "deterministic_closed_contract_multi_agent_research_governance_reference_only_no_external_agent_runtime_real_alpha_promotion_runtime_risk_execution_or_production_authority"
}
status_path = ROOT / "releases/history/strategy_factory/program/status/SAED_V4_32.json"
status_path.parent.mkdir(parents=True, exist_ok=True)
status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")

qa = {
    "phase": "SAED_V4_32",
    "title": "Multi Agent Research Constitution",
    "version": "1.0.0",
    "passed": True,
    "python_tests": python_tests,
    "closed_schema_pairs": len(list(SC.glob("*.SCHEMA.JSON"))),
    "golden_artifacts": len(list(AR.glob("*.JSON"))),
    "obsidian_notes": obsidian_notes,
    "phase_delivery_notes": phase_notes,
    "atomic_notes": atomic_notes,
    "mql5_static_files": mql5_files,
    "authority_boundary_passed": True,
    "deny_by_default_passed": True,
    "future_suffix_invariance_passed": True,
    "deterministic_replay_passed": True,
    "self_approval_mutations_rejected": True,
    "forbidden_capability_mutations_rejected": True,
    "protected_exposure_mutations_rejected": True,
    "budget_exhaustion_mutations_rejected": True,
    "counterexample_suppression_mutations_rejected": True,
    "claim_attribution_passed": True,
    "dissent_preservation_passed": True,
    "human_quorum_passed": True,
    "incident_containment_passed": True,
    "elapsed_seconds": elapsed,
    "external_evidence": {
        "external_agent_runtime": "not_claimed",
        "real_agent_collusion_resistance": "not_claimed",
        "metaeditor_compile": "pending_local_windows",
        "python_mql5_runtime_parity": "not_claimed",
        "broker_qualification": "not_claimed",
        "prospective_shadow": "not_claimed",
        "production_authorization": "not_claimed"
    }
}
(ROOT / "releases/history/saed/reports/SAED_V4_32_QA_REPORT.json").write_text(json.dumps(qa, indent=2, sort_keys=True) + "\n", encoding="utf-8")
runpy.run_path(str(tool / "validate_saed_v4_32_status.py"), run_name="__main__")
print(f"V4-32 full QA passed: {python_tests} tests, {qa['closed_schema_pairs']} schema pairs, {obsidian_notes} notes, {mql5_files} MQL5 static files")
