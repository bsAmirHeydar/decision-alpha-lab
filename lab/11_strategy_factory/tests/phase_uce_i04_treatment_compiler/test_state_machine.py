import pytest
from decimal import Decimal
from strategy_factory_treatment_compiler_v3.golden import compile_golden,path_scenarios
from strategy_factory_treatment_compiler_v3.state_machine import CausalPathStateMachine
from strategy_factory_treatment_compiler_v3.contracts import PathEvent
from strategy_factory_treatment_compiler_v3.enums import PathEventType,PathState
from strategy_factory_treatment_compiler_v3.errors import PathTransitionError
def test_all_golden_paths_close():
 t,_=compile_golden(); sm=CausalPathStateMachine()
 for events in path_scenarios(t).values(): assert sm.replay(t,events).state is PathState.CLOSED
def test_sequence_gap_rejected():
 t,_=compile_golden(); sm=CausalPathStateMachine(); s=sm.initial(t)
 with pytest.raises(PathTransitionError): sm.apply(s,PathEvent(2,PathEventType.SUBMIT,t.decision_time_ms,t.decision_time_ms))
def test_future_knowledge_rejected():
 t,_=compile_golden(); sm=CausalPathStateMachine(); s=sm.initial(t)
 with pytest.raises(PathTransitionError): sm.apply(s,PathEvent(1,PathEventType.SUBMIT,t.decision_time_ms+10,t.decision_time_ms))
def test_trail_cannot_loosen():
 t,_=compile_golden(); sm=CausalPathStateMachine(); evs=path_scenarios(t)['partial_trail_close'][:4]; s=sm.replay(t,evs)
 with pytest.raises(PathTransitionError): sm.apply(s,PathEvent(5,PathEventType.TRAIL_UPDATE,s.last_event_time_ms+1,s.last_known_time_ms+1,s.last_trail_price-Decimal('1'),Decimal('0'),'x','',{'side':'long'}))
