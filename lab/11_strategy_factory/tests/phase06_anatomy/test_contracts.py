import pytest
from strategy_factory_anatomy import AnatomyObservation,LifecycleRecord,ObservationKind,LifecycleState

def obs(**kw):
    d=dict(plugin_id='sf06.reference.sweep_rejection',plugin_version='1.0.0',symbol='EURUSD',timeframe_seconds=60,kind=ObservationKind.REFERENCE_SWEEP_HIGH,occurred_at_ms=1000,known_at_ms=1000,reference_price=1.1,extreme_price=1.101,close_price=1.099,source_bar_id='bar_1',source_hash='src_1',market_event_cluster_id='cluster_1')
    d.update(kw);return AnatomyObservation(**d)
def test_observation_stable_id():
    o=obs();o.validate();assert o.derived_id().startswith('obs_')
def test_future_known_rejected():
    with pytest.raises(ValueError):obs(known_at_ms=999).validate()
def test_id_mismatch_rejected():
    with pytest.raises(ValueError):obs(observation_id='obs_wrong').validate()
def test_lifecycle_valid():
    r=LifecycleRecord('obs_abc',1,LifecycleState.UNKNOWN,LifecycleState.OBSERVED,1000,'observed','src_1');r.validate();assert r.derived_id().startswith('life_')
def test_lifecycle_illegal():
    with pytest.raises(ValueError):LifecycleRecord('obs_abc',1,LifecycleState.UNKNOWN,LifecycleState.EMITTED,1000,'bad','src_1').validate()
