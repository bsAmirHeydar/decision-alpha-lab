import pytest
from strategy_factory_runtime import RuntimeState, RuntimeStateMachine

def test_legal_lifecycle():
    sm = RuntimeStateMachine()
    sm.transition(RuntimeState.INITIALIZING, 1, "init")
    sm.transition(RuntimeState.READY, 2, "ready")
    sm.transition(RuntimeState.RUNNING, 3, "run")
    sm.transition(RuntimeState.STOPPING, 4, "stop")
    sm.transition(RuntimeState.STOPPED, 5, "stopped")
    assert sm.state is RuntimeState.STOPPED

def test_illegal_transition_rejected():
    sm = RuntimeStateMachine()
    with pytest.raises(ValueError):
        sm.transition(RuntimeState.RUNNING, 1, "skip")
