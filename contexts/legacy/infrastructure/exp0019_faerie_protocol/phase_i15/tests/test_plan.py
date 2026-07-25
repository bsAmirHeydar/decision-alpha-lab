from dataclasses import replace
from fp_i15_paper import *
def test_buy_plan_ready(buy_plan): assert buy_plan.state==PlanState.READY
def test_sell_plan_ready(sell_plan): assert sell_plan.state==PlanState.READY
def test_protected_is_trade_symbol(buy_plan): assert buy_plan.trade_symbol=='ES'
def test_plan_deterministic(proof,buy_winner,readiness,buy_quote,buy_spec,risk,buy_plan): assert build_plan(proof,buy_winner,readiness,buy_quote,buy_spec,risk,buy_plan.created_utc_ms).plan_id==buy_plan.plan_id
def test_quote_changes_identity(proof,buy_winner,readiness,buy_quote,buy_spec,risk,buy_plan): assert build_plan(proof,buy_winner,readiness,replace(buy_quote,ask=100.5,quote_id='Q2'),buy_spec,risk,buy_plan.created_utc_ms).plan_id!=buy_plan.plan_id
def test_risk_changes_identity(proof,buy_winner,readiness,buy_quote,buy_spec,risk,buy_plan): assert build_plan(proof,buy_winner,readiness,buy_quote,buy_spec,replace(risk,fixed_risk_amount=200),buy_plan.created_utc_ms).plan_id!=buy_plan.plan_id
