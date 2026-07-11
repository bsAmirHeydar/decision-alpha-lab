from strategy_factory_outcome import *
from strategy_factory_outcome.fixtures import *
def test_outcome_id_stable():
    e=OutcomeEngine(SimulationPolicy(),registry(),"sf09.cost.fixture","1.0.0");e.register(candidate(),1000);e.process(bar(1,2000,100,104.5,99,104));a=e.pop()
    e=OutcomeEngine(SimulationPolicy(),registry(),"sf09.cost.fixture","1.0.0");e.register(candidate(),1000);e.process(bar(1,2000,100,104.5,99,104));b=e.pop();assert a.outcome_id==b.outcome_id
def test_net_equals_gross_minus_cost():
    e=OutcomeEngine(SimulationPolicy(),registry(.2),"sf09.cost.fixture","1.0.0");e.register(candidate(),1000);e.process(bar(1,2000,100,104.5,99,104));o=e.pop();assert abs(o.net_r-(o.gross_r-o.costs.total_cost_r))<1e-12
