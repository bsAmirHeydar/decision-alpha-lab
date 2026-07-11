import pytest
from strategy_factory_anatomy import *
def make_obs():return AnatomyObservation('sf06.reference.sweep_rejection','1.0.0','EURUSD',60,ObservationKind.REFERENCE_SWEEP_HIGH,1000,1000,1.1,1.101,1.099,'bar_1','src_1','cluster_1')
def test_duplicate_observation():
    l=AnatomyLedger();o=make_obs();l.append_observation(o)
    with pytest.raises(LedgerValidationError):l.append_observation(o)
def test_hash_chained_lifecycle():
    l=AnatomyLedger();r1=LifecycleRecord('obs_abc',1,LifecycleState.UNKNOWN,LifecycleState.OBSERVED,1000,'observed','src_1');r1=LifecycleRecord(**{**r1.__dict__,'lifecycle_id':r1.derived_id()}) if hasattr(r1,'__dict__') else r1
    # frozen/slots: reconstruct
    r1=LifecycleRecord('obs_abc',1,LifecycleState.UNKNOWN,LifecycleState.OBSERVED,1000,'observed','src_1','none')
    id1=r1.derived_id();r1=LifecycleRecord('obs_abc',1,LifecycleState.UNKNOWN,LifecycleState.OBSERVED,1000,'observed','src_1','none',id1)
    l.append_lifecycle(r1)
    r2=LifecycleRecord('obs_abc',2,LifecycleState.OBSERVED,LifecycleState.CONFIRMED,1001,'confirmed','src_1',id1)
    l.append_lifecycle(r2);l.validate()
def test_broken_chain_rejected():
    l=AnatomyLedger();r1=LifecycleRecord('obs_abc',1,LifecycleState.UNKNOWN,LifecycleState.OBSERVED,1000,'observed','src_1');l.append_lifecycle(r1)
    with pytest.raises(LedgerValidationError):l.append_lifecycle(LifecycleRecord('obs_abc',3,LifecycleState.OBSERVED,LifecycleState.CONFIRMED,1001,'confirmed','src_1','life_wrong'))
def test_duplicate_event():
    l=AnatomyLedger();l.append_event_id('evt_1')
    with pytest.raises(LedgerValidationError):l.append_event_id('evt_1')
