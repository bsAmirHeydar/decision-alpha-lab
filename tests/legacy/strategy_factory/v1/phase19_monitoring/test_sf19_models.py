import pytest
from strategy_factory_monitoring import *

def test_schema_manifest_is_deterministic():
    a=reference_schema();b=reference_schema();assert a.manifest_id==b.manifest_id;assert len(a.entries)==8

def test_duplicate_schema_name_rejected():
    e=reference_schema().entries[0]
    with pytest.raises(ValueError):TelemetrySchemaManifest("1",(e,e))

def test_event_known_time_is_causal():
    e=reference_schema().entries[0]
    with pytest.raises(ValueError):TelemetryEvent(e.metric_name,e.schema_id,"r","g","s","m","c","x",2,1,1,1.0)

def test_event_identity_stable():
    e=reference_schema().entries[0]
    args=(e.metric_name,e.schema_id,"r","g","s","m","c","x",1,2,1,1.0)
    assert TelemetryEvent(*args).event_id==TelemetryEvent(*args).event_id

def test_lifecycle_mutation_is_forbidden():
    with pytest.raises(ValueError):LifecycleRecommendation("x",LifecycleAction.SUSPEND,"s","m","g",1,(),(),True,True)
