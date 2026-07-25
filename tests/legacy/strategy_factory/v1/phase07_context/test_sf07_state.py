from strategy_factory_context.state import ContextState
from strategy_factory_contracts.records import FeatureValue
from strategy_factory_contracts.enums import FeatureType,FeatureQuality
from strategy_factory_contracts.time import MarketTimestamp

def feature(t):return FeatureValue('x','1.0.0',FeatureType.DOUBLE,FeatureQuality.VALID,t,'evt_x','src_x',1.0)
def test_state_generation_and_freshness():
    t=MarketTimestamp(1000);s=ContextState(4);s.begin_generation(7,'evt_x',t);s.put(feature(t),500);assert s.get('x').value==1.0;assert s.is_fresh('x',1500);assert not s.is_fresh('x',1501)
def test_dirty_state():
    t=MarketTimestamp(1000);s=ContextState(4);s.begin_generation(1,'evt_x',t);s.put(feature(t),100);s.mark_all_dirty();assert s.is_dirty('x')
def test_capacity():
    from pytest import raises
    t=MarketTimestamp(1000);s=ContextState(1);s.begin_generation(1,'evt_x',t);s.put(feature(t),0)
    with raises(ValueError):s.put(FeatureValue('y','1.0.0',FeatureType.DOUBLE,FeatureQuality.VALID,t,'evt_x','src_y',2.0),0)
