from __future__ import annotations
import json
from _common import ROOT
p=ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_32.json"
d=json.loads(p.read_text())
assert d["status"]=="accepted_reference" and d["qa_passed"]
for k in ["promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authorization","online_learning_authority","live_trading_authority"]: assert d[k] is False
assert d["external_agent_runtime"]=="not_claimed" and d["metaeditor_compile"]=="pending_local_windows"
print("V4-32 status validation passed")
