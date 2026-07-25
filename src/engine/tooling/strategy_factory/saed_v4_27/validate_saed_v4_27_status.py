from tools.repository_paths import find_repository_root
from pathlib import Path
import json
ROOT=find_repository_root(__file__)
s=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_27.json").read_text(encoding="utf-8"))
assert s["phase"]=="SAED_V4_27" and s["version"]=="1.0.0" and s["status"]=="accepted_reference" and s["qa_passed"]
assert s["python_tests"]==136 and s["closed_schemas"]==25 and s["obsidian_notes"]==247 and s["mql5_static_files"]==16 and s["golden_exact_artifacts"]==14
assert s["complete_trial_count"]==36 and s["complete_exposure_count"]==44 and s["multiplicity_family_count"]==6
assert s["next_phase"]=="SAED_V4_28" and s["metaeditor_compile"]=="pending_local_windows"
for f in ("real_alpha","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authorization","online_learning_authority","online_fdr_complete","hidden_evaluation_air_gap_complete"): assert s[f] is False,f
print("V4-27 phase status passed")
