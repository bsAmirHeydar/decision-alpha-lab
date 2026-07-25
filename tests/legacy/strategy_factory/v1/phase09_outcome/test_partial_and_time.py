from strategy_factory_outcome import *
from strategy_factory_outcome.fixtures import *
def test_partial_then_stop():
    e=OutcomeEngine(SimulationPolicy(),registry(),"sf09.cost.fixture","1.0.0");e.register(candidate(partial=.5),1000);e.process(bar(1,2000,100,104.5,99,103));assert e.pop() is None;e.process(bar(2,3000,103,103,97.5,98));o=e.pop();assert o.exit_reason==ExitReason.PARTIAL_TARGET_THEN_STOP;assert abs(o.gross_r-.5)<1e-12
def test_time_exit():
    e=OutcomeEngine(SimulationPolicy(),registry(),"sf09.cost.fixture","1.0.0");e.register(candidate(max_holding=1000),1000);e.process(bar(1,2000,100,101,99,100.5));e.process(bar(2,3000,100.5,101,100,100.5));o=e.pop();assert o.exit_reason==ExitReason.TIME
