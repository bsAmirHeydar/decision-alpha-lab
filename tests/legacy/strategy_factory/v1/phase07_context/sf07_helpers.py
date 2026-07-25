from strategy_factory_contracts.enums import Direction,TimestampPrecision,FeatureType
from strategy_factory_contracts.time import MarketTimestamp
from strategy_factory_contracts.records import AnatomyEvent
from strategy_factory_context.registry import FeatureRegistry
from strategy_factory_context.fixtures import fixture_nodes
from strategy_factory_context.descriptor import FeatureVectorSchema,VectorField
from strategy_factory_context.enums import MissingPolicy

def event(direction=Direction.LONG):
    t=MarketTimestamp(1783771260000,'UTC',0,'fixture',TimestampPrecision.MILLISECONDS)
    e=AnatomyEvent('', 'sf07_fixture','1.0.0','sf06.reference.sweep_rejection','1.0.0','EURUSD','EURUSD',direction,t,t,t,1.1,1.099,60,'fixture','none','cluster_fixture_007','source_fixture_007','confirmed')
    return e.with_derived_id()
def registry():
    r=FeatureRegistry()
    for n in fixture_nodes():r.register(n)
    return r
def vector_schema():
    return FeatureVectorSchema('sf07.reference_context_vector','1.0.0',(
        VectorField('event_direction',FeatureType.INTEGER,MissingPolicy.FAIL,0.0),VectorField('risk_distance',FeatureType.DOUBLE,MissingPolicy.FAIL,0.0),VectorField('normalized_risk',FeatureType.DOUBLE,MissingPolicy.FAIL,0.0),VectorField('conviction_seed',FeatureType.DOUBLE,MissingPolicy.FAIL,0.0)))
