from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.lifecycle import LifecycleMachine
from saed_v4_context_twin.enums import SupportStatus,TransitionDisposition,ContradictionSeverity

def machine(m):return LifecycleMachine(m.lifecycle_states,m.transition_rules,m.initial_lifecycle_state)
def test_apply(context_spec,seed):
 m=compile_twin(context_spec,seed);e=machine(m).request(m.twin_id,'initialized','r_initialize_valid','canonical_valid','2026-07-13T10:00:00Z',{'context_fresh','htf_alignment'},SupportStatus.SUPPORTED,[],['a'*64],1);assert e.disposition==TransitionDisposition.APPLIED and e.to_state=='valid'
def test_reject_missing(context_spec,seed):
 m=compile_twin(context_spec,seed);e=machine(m).request(m.twin_id,'initialized','r_initialize_valid','canonical_valid','2026-07-13T10:00:00Z',{'context_fresh'},SupportStatus.SUPPORTED,[],[],1);assert e.disposition==TransitionDisposition.REJECTED
def test_reject_support(context_spec,seed):
 m=compile_twin(context_spec,seed);e=machine(m).request(m.twin_id,'initialized','r_initialize_valid','canonical_valid','2026-07-13T10:00:00Z',{'context_fresh','htf_alignment'},SupportStatus.DEGRADED,[],[],1);assert e.disposition==TransitionDisposition.REJECTED
def test_reject_contradiction(context_spec,seed):
 m=compile_twin(context_spec,seed);e=machine(m).request(m.twin_id,'initialized','r_initialize_valid','canonical_valid','2026-07-13T10:00:00Z',{'context_fresh','htf_alignment'},SupportStatus.SUPPORTED,[ContradictionSeverity.CRITICAL],[],1);assert e.disposition==TransitionDisposition.REJECTED
