import pytest
from strategy_factory_outcome import *
from strategy_factory_outcome.fixtures import *

def engine(policy=None,cost=.0):return OutcomeEngine(policy or SimulationPolicy(),registry(cost),"sf09.cost.fixture","1.0.0")
def test_market_target():
    e=engine(cost=.05);e.register(candidate(),1000);e.process(bar(1,2000,100,101,99.5,100.5));e.process(bar(2,3000,100.5,104.5,100,104));o=e.pop();assert o.exit_reason==ExitReason.TARGET;assert o.gross_r==2;assert o.net_r<2;assert o.mfe_r>=2
def test_limit_fill_then_stop():
    e=engine();e.register(candidate(OrderKind.LIMIT,100,98,104),1000);e.process(bar(1,2000,101,101.5,99.5,100));e.process(bar(2,3000,100,100.5,97.5,98));o=e.pop();assert o.filled and o.exit_reason==ExitReason.STOP and o.gross_r==-1
def test_no_fill_expiration():
    e=engine();e.register(candidate(OrderKind.LIMIT,95,93,99),1000);e.process(bar(1,6000,100,101,99,100));o=e.pop();assert not o.filled and o.exit_reason==ExitReason.ENTRY_EXPIRED and o.net_r==0
def test_duplicate_candidate_rejected():
    e=engine();c=candidate();e.register(c,1000)
    with pytest.raises(ValueError):e.register(c,1000)
def test_duplicate_observation_idempotent():
    e=engine();e.register(candidate(),1000);o=bar(1,2000,100,101,99,100);e.process(o);e.process(o);assert e.telemetry["duplicates"]==1
def test_out_of_order_rejected():
    e=engine();e.register(candidate(),1000);e.process(bar(2,2000,100,101,99,100))
    with pytest.raises(ValueError):e.process(bar(1,3000,100,101,99,100))
