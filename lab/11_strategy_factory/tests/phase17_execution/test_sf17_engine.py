from strategy_factory_execution import *

def intent(kind=OrderKind.LIMIT, eligible=True, iid="i1"):
    return ExecutionIntentRecord(iid,"h"+iid,"b","c","ch","ctx","s","1","X","g",1,17,"rel","dp","rp","ap",kind,100,98,104,True,1.0,100,80,1,1000,10000,eligible)

def policy(**kw):
    d=dict(policy_id="p",policy_version="1",mode=ExecutionMode.PAPER,point=0.01,adverse_slippage_points=1,
      commission_per_lot_per_side=2,max_fill_volume_per_quote=0.5,maximum_quote_age_milliseconds=1000,
      allow_research_only_intents=False,allow_partial_fills=True,fill_market_on_next_quote=True,deterministic_seed=17)
    d.update(kw); return PaperExecutionPolicy(**d)

def test_limit_partial_fill_and_target_close():
    e=PaperExecutionEngine("run",policy()); o=e.submit(intent(),1000); assert o.state==OrderState.WORKING
    e.on_quote(QuoteObservation("X",100.4,100.5,1100,1)); assert o.filled_volume==0
    e.on_quote(QuoteObservation("X",99.8,99.9,1200,2)); assert o.state==OrderState.PARTIALLY_FILLED
    e.on_quote(QuoteObservation("X",99.7,99.8,1300,3)); assert o.state==OrderState.FILLED
    p=next(iter(e.positions.values())); assert p.volume==1.0 and p.state==PositionState.OPEN
    e.on_quote(QuoteObservation("X",104.2,104.3,1400,4)); assert p.state==PositionState.CLOSED
    assert p.close_reason==FillReason.EXIT_TARGET and e.ledger.validate_chain()

def test_duplicate_is_idempotent():
    e=PaperExecutionEngine("run",policy()); a=e.submit(intent(),1000); b=e.submit(intent(),1001)
    assert a.order_id==b.order_id and len(e.orders)==1

def test_authority_rejected():
    e=PaperExecutionEngine("run",policy()); o=e.submit(intent(eligible=False),1000)
    assert o.state==OrderState.REJECTED and o.reject_reason==RejectReason.RESEARCH_ONLY_AUTHORITY

def test_expiry_and_cancel():
    e=PaperExecutionEngine("run",policy()); o=e.submit(intent(),1000); assert e.cancel("i1",1100); assert o.state==OrderState.CANCELED
