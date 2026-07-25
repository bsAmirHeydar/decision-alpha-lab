from .contracts import *
def assert_plan(plan):
    assert plan.trade_symbol
    if plan.state==PlanState.READY:
        assert plan.geometry.status==GeometryStatus.READY and plan.sizing.status==GeometryStatus.READY
        assert plan.sizing.estimated_max_loss<=plan.sizing.risk_budget+1e-8
        if plan.direction==TradeDirection.SELL: assert abs(plan.geometry.adjusted_stop-(plan.geometry.raw_stop+plan.geometry.spread_snapshot))<=max(1e-8,plan.geometry.minimum_required_distance)
    return True
def assert_run(run):
    assert tuple(e.sequence for e in run.ledger)==tuple(range(1,len(run.ledger)+1))
    if run.position: assert run.order and run.order.state==OrderState.FILLED
    return True
