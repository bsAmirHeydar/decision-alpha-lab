from _common import ROOT,load
s=load(ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_33.json");assert s["qa_passed"] and s["status"]=="accepted_reference" and s["next_phase"]=="SAED_V4_34" and not s["production_authorization"]
print("V4-33 status passed")
