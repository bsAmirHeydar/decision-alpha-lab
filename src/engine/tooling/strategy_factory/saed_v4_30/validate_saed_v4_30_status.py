from __future__ import annotations
import json
from _common import ROOT,AR
status=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_30.json").read_text())
assert status["phase"]=="SAED_V4_30" and status["status"]=="accepted_reference" and status["qa_passed"]
assert status["python_tests"]>=200 and status["closed_schema_pairs"]==25 and status["golden_exact_artifacts"]==25
assert status["obsidian_notes"]==272 and status["phase_delivery_notes"]==181 and status["atomic_notes"]==90 and status["mql5_static_files"]==22
assert status["synthetic_logical_replication_complete"] and status["synthetic_lab_count"]==3 and status["one_run_per_lab"]
assert status["semantic_hash_reconciliation"]=="passed" and status["metric_tolerance_reconciliation"]=="passed"
assert status["independent_external_reproduction"]=="pending_external" and not status["external_institutional_replication_claim"]
for key in ["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authorization","online_learning_authority","live_trading_authority"]: assert status[key] is False,key
cert=json.loads((AR/"GOLDEN_INDEPENDENT_MULTI_LAB_REPLICATION_CERTIFICATE.JSON").read_text()); handoff=json.loads((AR/"V4_30_TO_V4_31_HANDOFF.JSON").read_text())
assert status["certificate_hash"]==cert["certificate_hash"] and status["handoff_hash"]==handoff["handoff_hash"] and status["next_phase"]=="SAED_V4_31"
print("V4-30 phase status validation passed")
