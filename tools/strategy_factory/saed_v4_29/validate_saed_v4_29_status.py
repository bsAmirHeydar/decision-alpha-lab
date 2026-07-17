from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3]; s=json.loads((ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_29.json").read_text(encoding="utf-8"))
assert s["phase"]=="SAED_V4_29" and s["version"]=="1.0.0" and s["qa_passed"] and s["status"]=="accepted_reference"
assert s["hidden_evaluation_air_gap_reference_complete"] and s["one_shot_evaluation_count"]==1 and s["researcher_hidden_label_reads"]==0
for k in ["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authorization","online_learning_authority","live_trading_authority","real_hidden_dataset_claim","independent_replication_claim"]: assert s[k] is False,k
print("V4-29 phase status validation passed")
