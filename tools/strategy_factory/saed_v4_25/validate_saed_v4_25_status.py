from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
status = json.loads((ROOT / "lab/11_strategy_factory/phase_status/SAED_V4_25.json").read_text(encoding="utf-8"))
assert status["phase"] == "SAED_V4_25" and status["version"] == "1.0.0"
assert status["status"] == "accepted_reference" and status["qa_passed"]
assert status["python_tests"] >= 170
assert status["closed_schemas"] == 36 and status["closed_schema_pairs"] == 36
assert status["obsidian_notes"] == 255 and status["mql5_static_files"] == 22
assert status["golden_exact_artifacts"] == 20
assert status["metaeditor_compile"] == "pending_local_windows"
assert status["runtime_parity"] == "not_claimed"
assert status["real_alpha"] is False
assert status["promotion_authority"] is False
assert status["runtime_executable"] is False
assert status["risk_allocation_authority"] is False
assert status["execution_authority"] is False
assert status["production_authorization"] is False
assert status["online_learning_authority"] is False
assert status["next_phase"] == "SAED_V4_26"
print("V4-25 phase status validation passed")
