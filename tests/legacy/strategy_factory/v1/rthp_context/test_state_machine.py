from src.engine.tooling.strategy_factory.contexts.rthp.state_machine import ReferenceStateMachine
from src.engine.tooling.strategy_factory.contexts.rthp.models import ReferenceState
def test_confirm_then_exhaust():
 s=ReferenceStateMachine();assert s.first_touch("A","B")==ReferenceState.ONE_SIDE_TOUCHED;assert s.confirm()==ReferenceState.DIVERGENCE_CONFIRMED;assert s.protected_touch()==ReferenceState.REFERENCE_EXHAUSTED
