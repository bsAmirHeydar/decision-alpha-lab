from strategy_factory_monitoring import *

def coordinator(cap=128):
    schema=reference_schema();dash=reference_dashboard();manifest=reference_manifest(capacity=cap);return MonitoringCoordinator(manifest,schema,dash,reference_latency_policies(),reference_alert_policies()),schema,manifest

def test_coordinator_accepts_exact_schema():
    c,s,m=coordinator();e=s.entries[0];x=TelemetryEvent(e.metric_name,e.schema_id,m.run_id,m.generation_id,m.strategy_id,m.model_id,"c","x",1,1,1,100);assert c.ingest(x);assert c.report(2).telemetry_count==1

def test_schema_mismatch_fails_closed():
    c,s,m=coordinator();e=s.entries[0];x=TelemetryEvent(e.metric_name,"wrong",m.run_id,m.generation_id,m.strategy_id,m.model_id,"c","x",1,1,1,100);assert not c.ingest(x);assert c.report(2).health.schema_rejection_count==1

def test_shifted_drift_changes_health():
    c,_,_=coordinator();c.evaluate_distribution(reference_baseline(),reference_observation(True),reference_drift_policy());r=c.report(10);assert r.health.state in {HealthState.DEGRADED,HealthState.CRITICAL};assert r.recommendation.requires_operator_approval;assert not r.recommendation.automatic_mutation_allowed

def test_reconciliation_mismatch_recommends_suspend():
    c,_,_=coordinator();o=ExecutionDriftObservation("o",1,2,100,90,2,1,1,2,100,200,0);c.evaluate_execution(o,reference_execution_policy());r=c.report(3);assert r.health.state==HealthState.SUSPEND_RECOMMENDED;assert r.recommendation.action==LifecycleAction.SUSPEND

def test_integrity_failure_recommends_rollback_not_executes_it():
    c,_,_=coordinator();c.add_integrity_failure("MODEL_INTEGRITY_FAILURE");r=c.report(3);assert r.recommendation.action==LifecycleAction.ROLLBACK;assert r.recommendation.requires_operator_approval;assert not r.recommendation.automatic_mutation_allowed

def test_ring_drop_degrades_health():
    c,s,m=coordinator(1)
    for i in (1,2):
        e=s.entries[0];assert c.ingest(TelemetryEvent(e.metric_name,e.schema_id,m.run_id,m.generation_id,m.strategy_id,m.model_id,f"c{i}","x",i,i,i,100))
    assert c.report(3).health.state==HealthState.DEGRADED
