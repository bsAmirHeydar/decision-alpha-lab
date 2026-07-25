from _common import ROOT,load
s=load(ROOT/"releases/history/strategy_factory/program/status/SAED_V4_33.json");assert s["qa_passed"] and s["status"]=="accepted_reference" and s["next_phase"]=="SAED_V4_34" and not s["production_authorization"]
print("V4-33 status passed")
