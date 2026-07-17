from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]; s=json.loads((ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_28.json").read_text(encoding="utf-8"))
assert s["phase"]=="SAED_V4_28" and s["version"]=="1.0.0" and s["qa_passed"] and s["status"]=="accepted_reference"
assert s["online_fdr_reference_complete"] and not s["real_world_fdr_guarantee"] and not s["hidden_evaluation_air_gap_complete"]
assert not any(s[k] for k in ["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authorization","online_learning_authority"])
print("V4-28 status validation passed")
