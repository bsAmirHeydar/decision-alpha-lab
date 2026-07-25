from __future__ import annotations
import pytest
from dataclasses import replace
from strategy_factory_contexts_v3 import *
from strategy_factory_contexts_v3.fixtures import synthetic_records

def observation():
    return SyntheticBreakContextPackage().observe(synthetic_records()[0])[0]

def test_duplicate_suppression_and_collision():
    e=ContextLifecycleEngine(2); o=observation()
    current,is_new=e.register(o); assert is_new and current==o
    current,is_new=e.register(o); assert not is_new and e.duplicates_suppressed==1
    corrupt=replace(o,payload={**o.payload,"close":2.0})
    with pytest.raises(LifecycleError): e.register(corrupt)

def test_legal_lifecycle_path():
    e=ContextLifecycleEngine(); o=observation(); e.register(o)
    active=e.transition(o.observation_id,ContextLifecycleState.ACTIVE,UtcInstant(o.time_chain.known_time.epoch_ms+1),"activated")
    assert active.lifecycle_state==ContextLifecycleState.ACTIVE
    expired=e.transition(o.observation_id,ContextLifecycleState.EXPIRED,UtcInstant(o.time_chain.known_time.epoch_ms+2),"expired")
    retired=e.transition(o.observation_id,ContextLifecycleState.RETIRED,UtcInstant(o.time_chain.known_time.epoch_ms+3),"retired")
    assert retired.lifecycle_state==ContextLifecycleState.RETIRED
    assert len(e.transitions)==3

def test_illegal_transition_and_time_reversal():
    e=ContextLifecycleEngine(); o=observation(); e.register(o)
    with pytest.raises(LifecycleError): e.transition(o.observation_id,ContextLifecycleState.DETECTED,UtcInstant(o.time_chain.known_time.epoch_ms+1),"rewind")
    with pytest.raises(LifecycleError): e.transition(o.observation_id,ContextLifecycleState.ACTIVE,UtcInstant(o.time_chain.known_time.epoch_ms-1),"past")

def test_supersession_links_both_records():
    e=ContextLifecycleEngine(); old=observation(); e.register(old)
    source=dict(synthetic_records()[0]); source.update(source_event_id="evt.synthetic.replacement",signal_bar_open_ms=source["signal_bar_open_ms"]+60000,event_time_ms=source["event_time_ms"]+60000,known_time_ms=source["known_time_ms"]+60000,confirmation_time_ms=source["confirmation_time_ms"]+60000,observation_cut_ms=source["observation_cut_ms"]+60000,decision_time_ms=source["decision_time_ms"]+60000)
    new=SyntheticBreakContextPackage().observe(source)[0]
    old2,new2=e.supersede(old.observation_id,new,UtcInstant(source["known_time_ms"]),"replacement")
    assert old2.lifecycle_state==ContextLifecycleState.SUPERSEDED
    assert new2.supersedes_observation_id==old.observation_id

def test_capacity_fails_closed():
    e=ContextLifecycleEngine(1); e.register(observation())
    source=dict(synthetic_records()[0]); source.update(source_event_id="evt.2",signal_bar_open_ms=1710000060000,event_time_ms=1710000119999,known_time_ms=1710000120000,confirmation_time_ms=1710000120000,observation_cut_ms=1710000120000,decision_time_ms=1710000120001)
    with pytest.raises(LifecycleError): e.register(SyntheticBreakContextPackage().observe(source)[0])
