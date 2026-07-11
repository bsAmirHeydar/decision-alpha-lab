from dataclasses import dataclass
from strategy_factory_contracts.enums import FeatureType,FeatureQuality
from strategy_factory_contracts.records import FeatureValue,AnatomyEvent
from .descriptor import FeatureDescriptor
from .enums import UpdateScope
class EventDirectionNode:
    descriptor=FeatureDescriptor('event_direction','1.0.0','sf07.fixture.event_direction',FeatureType.INTEGER,UpdateScope.EVENT,True,True)
    def compute(self,event,state):return FeatureValue('event_direction','1.0.0',FeatureType.INTEGER,FeatureQuality.VALID,event.known_time,event.event_id,'sf07_direction',int(event.direction))
class RiskDistanceNode:
    descriptor=FeatureDescriptor('risk_distance','1.0.0','sf07.fixture.risk_distance',FeatureType.DOUBLE,UpdateScope.EVENT,True,True)
    def compute(self,event,state):return FeatureValue('risk_distance','1.0.0',FeatureType.DOUBLE,FeatureQuality.VALID,event.known_time,event.event_id,'sf07_risk',abs(event.reference_price-event.invalidation_price))
class ReferenceMagnitudeNode:
    descriptor=FeatureDescriptor('reference_magnitude','1.0.0','sf07.fixture.reference_magnitude',FeatureType.DOUBLE,UpdateScope.EVENT,True,True)
    def compute(self,event,state):return FeatureValue('reference_magnitude','1.0.0',FeatureType.DOUBLE,FeatureQuality.VALID,event.known_time,event.event_id,'sf07_reference',abs(event.reference_price))
class NormalizedRiskNode:
    descriptor=FeatureDescriptor('normalized_risk','1.0.0','sf07.fixture.normalized_risk',FeatureType.DOUBLE,UpdateScope.EVENT,True,True,0,('risk_distance','reference_magnitude'))
    def compute(self,event,state):
        r=state.get('risk_distance');m=state.get('reference_magnitude');return FeatureValue('normalized_risk','1.0.0',FeatureType.DOUBLE,FeatureQuality.VALID,event.known_time,event.event_id,'sf07_normalized',float(r.value)/float(m.value))
class ConvictionSeedNode:
    descriptor=FeatureDescriptor('conviction_seed','1.0.0','sf07.fixture.conviction_seed',FeatureType.DOUBLE,UpdateScope.EVENT,True,True,0,('event_direction','normalized_risk'))
    def compute(self,event,state):
        d=state.get('event_direction');n=state.get('normalized_risk');sign=1.0 if int(d.value)>=0 else -1.0;return FeatureValue('conviction_seed','1.0.0',FeatureType.DOUBLE,FeatureQuality.VALID,event.known_time,event.event_id,'sf07_conviction',sign/(1.0+float(n.value)))
def fixture_nodes():return (EventDirectionNode(),RiskDistanceNode(),ReferenceMagnitudeNode(),NormalizedRiskNode(),ConvictionSeedNode())
