from __future__ import annotations
import json
from _common import ROOT
status=json.loads((ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_31.json").read_text()); qa=json.loads((ROOT/"releases/history/saed/reports/SAED_V4_31_QA_REPORT.json").read_text())
assert status["phase"]=="SAED_V4_31" and status["qa_passed"] and qa["passed"]
assert status["python_tests"]>=180 and status["closed_schema_pairs"]==31 and status["obsidian_notes"]>=250 and status["mql5_static_files"]==22
assert status["mutation_score"]==1.0 and status["proof_obligations_all_discharged"] and status["safety_case_valid"]
assert not status["production_authorization"] and not status["execution_authority"] and status["next_phase"]=="SAED_V4_32"
print("V4-31 phase status validation passed")
