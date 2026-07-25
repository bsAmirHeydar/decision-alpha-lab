from __future__ import annotations
from .models import LifecycleStateDefinition,TransitionRule,TransitionEvent
from .enums import TransitionDisposition,SupportStatus,ContradictionSeverity
from .errors import LifecycleError

class LifecycleMachine:
    def __init__(self,states,rules,initial_state):
        self.states={x.state_id:x for x in states};self.rules={x.rule_id:x for x in rules}
        if initial_state not in self.states:raise LifecycleError('unknown initial state')
        for r in rules:
            if r.from_state not in self.states or r.to_state not in self.states:raise LifecycleError('rule references unknown state')
            if self.states[r.from_state].terminal:raise LifecycleError('transition from terminal state')
        self.initial_state=initial_state
    def request(self,twin_id,current_state,rule_id,trigger,known_time,available_observables,support_status,active_severities,evidence_hashes,sequence):
        r=self.rules.get(rule_id)
        reasons=[]
        if not r:raise LifecycleError('unknown rule')
        if current_state!=r.from_state:reasons.append('from_state_mismatch')
        if trigger!=r.trigger:reasons.append('trigger_mismatch')
        missing=sorted(set(r.required_observables)-set(available_observables))
        if missing:reasons.append('missing_observables:'+','.join(missing))
        if r.requires_support and support_status!=SupportStatus.SUPPORTED:reasons.append('support_not_supported')
        forbidden=set(r.forbidden_contradiction_severities)&{x.value if hasattr(x,'value') else str(x) for x in active_severities}
        if forbidden:reasons.append('forbidden_contradiction:'+','.join(sorted(forbidden)))
        if r.review_required and not reasons:disp=TransitionDisposition.REVIEW
        elif reasons:disp=TransitionDisposition.REJECTED
        elif r.to_state==current_state:disp=TransitionDisposition.NOOP
        else:disp=TransitionDisposition.APPLIED
        to_state=r.to_state if disp==TransitionDisposition.APPLIED else current_state
        return TransitionEvent(twin_id,rule_id,current_state,to_state,known_time,trigger,tuple(sorted(evidence_hashes)),disp,tuple(reasons),sequence)
