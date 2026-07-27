import pytest
from strategy_factory_context.registry import FeatureRegistry,FeatureGraphError
from strategy_factory_context.descriptor import FeatureDescriptor
from strategy_factory_context.enums import UpdateScope
from strategy_factory_contracts.enums import FeatureType,FeatureQuality
from strategy_factory_contracts.records import FeatureValue
from .sf07_helpers import registry
class Node:
    def __init__(self,d):self.descriptor=d
    def compute(self,event,state):return FeatureValue(self.descriptor.feature_id,self.descriptor.feature_version,self.descriptor.value_type,FeatureQuality.VALID,event.known_time,event.event_id,'x',1.0)
def test_deterministic_topological_order():
    r=registry();assert r.compile()==('event_direction','reference_magnitude','risk_distance','normalized_risk','conviction_seed');assert r.graph_hash.startswith('fdag_')
def test_duplicate_owner_rejected():
    r=registry()
    with pytest.raises(FeatureGraphError):r.register(r.node('event_direction'))
def test_missing_dependency_rejected():
    r=FeatureRegistry();r.register(Node(FeatureDescriptor('a','1.0.0','x',FeatureType.DOUBLE,UpdateScope.EVENT,True,True,0,('missing',))))
    with pytest.raises(FeatureGraphError):r.compile()
def test_cycle_rejected():
    r=FeatureRegistry();r.register(Node(FeatureDescriptor('a','1.0.0','x',FeatureType.DOUBLE,dependencies=('b',))));r.register(Node(FeatureDescriptor('b','1.0.0','x',FeatureType.DOUBLE,dependencies=('a',))))
    with pytest.raises(FeatureGraphError):r.compile()
