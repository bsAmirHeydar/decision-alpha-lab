from fp_i15_paper import *
def test_reconciled_risk_within_cap(buy_plan,buy_quote,buy_spec):
 r=simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms,fill_slippage_price=buy_plan.geometry.worst_case_entry-buy_plan.geometry.planned_entry); x=reconcile_risk(buy_plan,r.position,buy_spec); assert x['within_cap']
def test_no_position_reconciles(buy_plan,buy_spec): assert reconcile_risk(buy_plan,None,buy_spec)['status']=='NO_POSITION'
def test_stop_close_pnl_negative(buy_plan,buy_quote,buy_spec):
 r=simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);p=close_position(r.position,buy_spec,r.position.stop,buy_plan.created_utc_ms+100,PositionState.CLOSED_STOP);assert p.realized_pnl<0
def test_target_close_pnl_positive(buy_plan,buy_quote,buy_spec):
 r=simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);p=close_position(r.position,buy_spec,r.position.target,buy_plan.created_utc_ms+100,PositionState.CLOSED_TARGET);assert p.realized_pnl>0
