from strategy_factory_context.engine import ContextEngine
from sf07_helpers import registry,vector_schema,event

def test_end_to_end_context_build():
    engine=ContextEngine(registry(),vector_schema());snapshot,frame,vector=engine.build(event(),7)
    assert len(snapshot.values)==5 and frame.feature_count==5 and len(vector.values)==4
    assert vector.feature_ids==('event_direction','risk_distance','normalized_risk','conviction_seed')
    assert vector.values[0]==1.0 and frame.frame_id==frame.derived_id
    assert engine.telemetry.build_count==1 and engine.telemetry.feature_computations==5
def test_repeat_is_deterministic():
    engine=ContextEngine(registry(),vector_schema());a=engine.build(event(),7);b=engine.build(event(),7)
    assert a[0].snapshot_id==b[0].snapshot_id and a[1].frame_id==b[1].frame_id and a[2].vector_id==b[2].vector_id
