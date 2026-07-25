from __future__ import annotations
import json
from _common import ROOT
s=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_34.json").read_text()); assert s["status"]=="accepted_reference" and s["qa_passed"] and s["production_authorization"] is False and s["next_phase"]=="SAED_V4_35"
print("V4-34 status validation passed")
