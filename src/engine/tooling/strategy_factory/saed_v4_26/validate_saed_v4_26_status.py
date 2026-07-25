from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__); s=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_26.json").read_text())
assert s["phase"]=="SAED_V4_26" and s["status"]=="accepted_reference" and s["qa_passed"] and s["next_phase"]=="SAED_V4_27"
assert s["closed_schemas"]==39 and s["obsidian_notes"]==323 and s["mql5_static_files"]==25
for f in ["real_alpha","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authorization","online_learning_authority"]: assert s[f] is False
print("V4-26 phase status validation passed")
