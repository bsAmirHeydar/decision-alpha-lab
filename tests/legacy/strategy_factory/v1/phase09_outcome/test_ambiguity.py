from strategy_factory_outcome import *
from strategy_factory_outcome.fixtures import *
def run(policy):
    e=OutcomeEngine(policy,registry(),"sf09.cost.fixture","1.0.0");e.register(candidate(),1000);e.process(bar(1,2000,100,104.5,97.5,100));return e.pop()
def test_stop_first():assert run(SimulationPolicy(ambiguity=AmbiguityPolicy.STOP_FIRST)).exit_reason==ExitReason.STOP
def test_target_first():assert run(SimulationPolicy(ambiguity=AmbiguityPolicy.TARGET_FIRST)).exit_reason==ExitReason.TARGET
def test_exclude():
    o=run(SimulationPolicy(ambiguity=AmbiguityPolicy.EXCLUDE));assert o.exit_reason==ExitReason.AMBIGUOUS_BAR and o.ambiguous
def test_require_lower_fidelity():assert run(SimulationPolicy(ambiguity=AmbiguityPolicy.REQUIRE_LOWER_FIDELITY)).terminal_state==RuntimeState.AMBIGUOUS
