from fp_i15_paper import *
def test_immediate_fill_opens_position(buy_plan,buy_quote):
 r=simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms); assert r.order.state==OrderState.FILLED and r.position.state==PositionState.OPEN
def test_partial_then_fill_has_two_fills(buy_plan,buy_quote):
 r=simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.PARTIAL_THEN_FILL,buy_quote,buy_plan.created_utc_ms); assert len(r.fills)==2 and r.order.state==OrderState.FILLED
def test_cancel_no_position(buy_plan,buy_quote): assert simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.ACCEPT_THEN_CANCEL,buy_quote,buy_plan.created_utc_ms).position is None
def test_quote_unavailable_no_order(buy_plan,buy_quote): assert simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.QUOTE_UNAVAILABLE,buy_quote,buy_plan.created_utc_ms).order is None
def test_geometry_drift_no_order(buy_plan,buy_quote): assert simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.GEOMETRY_DRIFT,buy_quote,buy_plan.created_utc_ms).order is None
def test_ledger_sequence(buy_plan,buy_quote):
 r=simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms); assert [e.sequence for e in r.ledger]==list(range(1,len(r.ledger)+1))
def test_run_deterministic(buy_plan,buy_quote):
 p=paper_policy(PaperPolicyProfile.FILLED);a=simulate(buy_plan,p,PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);b=simulate(buy_plan,p,PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms);assert a.run_hash==b.run_hash
