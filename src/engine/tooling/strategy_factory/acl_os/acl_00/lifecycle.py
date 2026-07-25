from __future__ import annotations
from .catalogs import PolicyBundle
from .types import LifecycleState,Reason,TransitionRequest

class LifecycleEvaluator:
    def __init__(self,bundle:PolicyBundle): self.bundle=bundle
    def policy_for(self,request:TransitionRequest)->tuple[dict|None,list[Reason]]:
        if request.from_state==LifecycleState.RETIRED:
            return None,[Reason("TERMINAL_STATE","RETIRED is terminal and has no outgoing transition.","LIFECYCLE_TERMINAL",False)]
        policy=self.bundle.transition(request.from_state.value,request.to_state.value)
        if policy is None: return None,[Reason("TRANSITION_NOT_ALLOWED",f"Transition {request.from_state.value}->{request.to_state.value} is not registered.","LIFECYCLE_TRANSITION_GRAPH",False)]
        if request.from_state==request.to_state: return None,[Reason("NOOP_TRANSITION_FORBIDDEN","State transition must change state.","LIFECYCLE_NOOP",False)]
        return policy,[]
