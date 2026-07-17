import copy,pytest
from saed_v4_prospective_shadow_micro_live.modes import transition
from saed_v4_prospective_shadow_micro_live.risk import evaluate_intent
from saed_v4_prospective_shadow_micro_live.errors import ModeError

def test_off_to_paper(output):
 x=transition("OFF","PAPER",output["mode_ladder"],{"RUNTIME_HASH_BOUND","COHORT_FROZEN"},False);assert x["to_mode"]=="PAPER" and x["side_effects_allowed"] is False

def test_skip_stage_fails(output):
 with pytest.raises(ModeError):transition("OFF","SHADOW",output["mode_ladder"],set(),False)
def test_micro_qualification_requires_manual(output):
 gates={"ACTUAL_PAPER_PASS","ACTUAL_SHADOW_PASS","METAEDITOR_PASS","TERMINAL_PARITY_PASS","DEMO_BROKER_PASS"}
 with pytest.raises(ModeError):transition("SHADOW","MICRO_LIVE_QUALIFICATION",output["mode_ladder"],gates,False)
def test_micro_live_requires_all(output):
 with pytest.raises(ModeError):transition("MICRO_LIVE_QUALIFICATION","MICRO_LIVE",output["mode_ladder"],{"SIGNED_MICRO_LIVE_PERMIT"},True)
@pytest.mark.parametrize("field,value,reason",[("risk_fraction",.006,"TRADE_RISK_CAP"),("size_fraction",.02,"SIZE_CAP"),("spread_bps",9.0,"SPREAD_CAP"),("latency_ms",1001,"LATENCY_CAP")])
def test_intent_caps(output,field,value,reason):
 i=copy.deepcopy(output["intent_ledger"]["events"][1]);i[field]=value;s={"orders_today":0,"concurrent_positions":0,"daily_loss_fraction":0.0,"drawdown_fraction":0.0,"kill_switch_armed":True};r=evaluate_intent(i,output["risk_envelope"],s);assert r["passed"] is False and reason in r["reasons"]
@pytest.mark.parametrize("state_field,state_value,reason",[("orders_today",3,"ORDER_COUNT_CAP"),("concurrent_positions",1,"CONCURRENCY_CAP"),("daily_loss_fraction",.01,"DAILY_LOSS_CAP"),("drawdown_fraction",.02,"DRAWDOWN_CAP"),("kill_switch_armed",False,"KILL_SWITCH_NOT_ARMED")])
def test_state_caps(output,state_field,state_value,reason):
 i=copy.deepcopy(output["intent_ledger"]["events"][1]);i["decision"]="SELECT";i["risk_fraction"]=.001;i["size_fraction"]=.005;i["spread_bps"]=1;i["latency_ms"]=10;s={"orders_today":0,"concurrent_positions":0,"daily_loss_fraction":0.0,"drawdown_fraction":0.0,"kill_switch_armed":True};s[state_field]=state_value;r=evaluate_intent(i,output["risk_envelope"],s);assert r["passed"] is False and reason in r["reasons"]
