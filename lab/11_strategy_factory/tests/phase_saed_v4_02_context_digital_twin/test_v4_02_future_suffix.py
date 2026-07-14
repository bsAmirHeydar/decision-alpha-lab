from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.observations import ObservationLedger
from saed_v4_context_twin.models import Observation
from saed_v4_context_twin.enums import ObservationKind
from saed_v4_context_twin.state import build_snapshot
H='a'*64

def make(twin, value, known, seq):
    return Observation(twin,'volatility_z',value,'2026-07-13T09:00:00Z',known,'art',H,ObservationKind.DERIVED_FACT,1.0,seq)

def test_future_observation_not_visible_in_past(context_spec,seed):
    m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables)
    l.append(make(m.twin_id,0.1,'2026-07-13T10:00:00Z',1))
    before=l.visible(m.twin_id,'2026-07-13T10:00:01Z')
    l.append(make(m.twin_id,0.9,'2026-07-14T10:00:00Z',2))
    after=l.visible(m.twin_id,'2026-07-13T10:00:01Z')
    assert [x.observation_id for x in before]==[x.observation_id for x in after]

def test_future_suffix_does_not_change_past_snapshot(context_spec,seed):
    m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables)
    l.append(make(m.twin_id,0.1,'2026-07-13T10:00:00Z',1))
    obs1=l.visible(m.twin_id,'2026-07-13T10:00:01Z')
    s1=build_snapshot(m,'2026-07-13T10:00:01Z','initialized',obs1,(),None,(),(),(),1)
    l.append(make(m.twin_id,0.9,'2026-07-14T10:00:00Z',2))
    obs2=l.visible(m.twin_id,'2026-07-13T10:00:01Z')
    s2=build_snapshot(m,'2026-07-13T10:00:01Z','initialized',obs2,(),None,(),(),(),1)
    assert s1.snapshot_hash==s2.snapshot_hash

def test_future_observation_visible_after_boundary(context_spec,seed):
    m=compile_twin(context_spec,seed);l=ObservationLedger(m.observables)
    l.append(make(m.twin_id,0.1,'2026-07-13T10:00:00Z',1));l.append(make(m.twin_id,0.9,'2026-07-14T10:00:00Z',2))
    assert len(l.visible(m.twin_id,'2026-07-14T10:00:01Z'))==2
