from __future__ import annotations
from .enums import DriftKind,MetricKind
from .hashing import stable_id
from .models import *

def reference_schema()->TelemetrySchemaManifest:
    entries=(
        TelemetrySchemaEntry("latency.pipeline_us","1.0.0",MetricKind.HISTOGRAM,"microseconds","pipeline","End-to-end event to decision latency",0,10_000_000,("strategy_id","model_id")),
        TelemetrySchemaEntry("latency.inference_us","1.0.0",MetricKind.HISTOGRAM,"microseconds","inference","ONNX inference latency",0,10_000_000,("model_id",)),
        TelemetrySchemaEntry("latency.execution_us","1.0.0",MetricKind.HISTOGRAM,"microseconds","execution","Intent to broker acknowledgement latency",0,60_000_000,("symbol",)),
        TelemetrySchemaEntry("drift.feature.psi","1.0.0",MetricKind.GAUGE,"ratio","drift","Feature PSI",0,100,()),
        TelemetrySchemaEntry("drift.prediction.psi","1.0.0",MetricKind.GAUGE,"ratio","drift","Prediction PSI",0,100,()),
        TelemetrySchemaEntry("drift.execution.reject_rate","1.0.0",MetricKind.GAUGE,"ratio","execution","Broker reject rate",0,1,()),
        TelemetrySchemaEntry("reconciliation.mismatch_count","1.0.0",MetricKind.COUNTER,"count","reconciliation","Unresolved broker reconciliation mismatches",0,None,()),
        TelemetrySchemaEntry("runtime.queue_depth","1.0.0",MetricKind.GAUGE,"count","runtime","Bounded queue depth",0,100000,()),
    )
    return TelemetrySchemaManifest("1.0.0",entries)

def reference_dashboard(now_ms:int=1_700_000_000_000)->DashboardSpec:
    panels=(
        DashboardPanel("health","Runtime Health",("runtime.queue_depth","reconciliation.mismatch_count"),"status",1000),
        DashboardPanel("latency","Latency P50/P95/P99",("latency.pipeline_us","latency.inference_us","latency.execution_us"),"histogram",5000),
        DashboardPanel("drift","Feature Prediction Execution Drift",("drift.feature.psi","drift.prediction.psi","drift.execution.reject_rate"),"timeseries",60000),
    )
    return DashboardSpec("sf19-reference-dashboard","1.0.0",panels,now_ms)

def reference_manifest(now_ms:int=1_700_000_000_000,capacity:int=128)->MonitoringRunManifest:
    schema=reference_schema();dash=reference_dashboard(now_ms)
    return MonitoringRunManifest("run-phase19-reference","generation-phase19-reference","strategy-reference","model-reference",schema.manifest_id,dash.dashboard_id,now_ms,capacity)

def reference_latency_policies()->tuple[LatencySloPolicy,...]:
    edges=(100,250,500,1_000,2_500,5_000,10_000,25_000,50_000,100_000,250_000,1_000_000)
    return (
        LatencySloPolicy("slo-pipeline-v1","pipeline",edges,5_000,25_000,100_000,5),
        LatencySloPolicy("slo-inference-v1","inference",edges,1_000,5_000,10_000,5),
        LatencySloPolicy("slo-execution-v1","execution",edges,50_000,250_000,1_000_000,5),
    )

def reference_alert_policies()->tuple[AlertPolicy,...]:
    return (
        AlertPolicy("alert-feature-psi-v1","drift.feature.psi",.10,.25,"HIGH",2,2,0,300000),
        AlertPolicy("alert-prediction-psi-v1","drift.prediction.psi",.10,.25,"HIGH",2,2,0,300000),
        AlertPolicy("alert-reject-rate-v1","drift.execution.reject_rate",.05,.15,"HIGH",2,2,0,300000),
        AlertPolicy("alert-reconciliation-v1","reconciliation.mismatch_count",1,1,"HIGH",1,2,0,60000),
        AlertPolicy("alert-queue-v1","runtime.queue_depth",100,500,"HIGH",2,2,0,300000),
    )

def reference_drift_policy(kind:DriftKind=DriftKind.FEATURE)->DriftThresholdPolicy:
    return DriftThresholdPolicy(f"drift-policy-{kind.value.lower()}-v1",kind,.10,.25,.03,.10,1.0,2.0,.05,.01,100)

def reference_baseline(kind:DriftKind=DriftKind.FEATURE)->DriftBaseline:
    name="feature.volatility_z" if kind==DriftKind.FEATURE else "prediction.trade_probability"
    return DriftBaseline(f"baseline-{kind.value.lower()}-v1",kind,name,"model-reference",(-1.0,0.0,1.0),(.10,.40,.40,.10),0.0,1.0,1000,1_699_000_000_000,1_699_100_000_000)

def reference_observation(shifted:bool=False,kind:DriftKind=DriftKind.FEATURE)->DriftObservation:
    b=reference_baseline(kind);counts=(5,15,30,150) if shifted else (10,40,40,10);mean=2.2 if shifted else .05
    return DriftObservation(stable_id("obs",kind.value,shifted),b.baseline_id,kind,b.feature_name,b.model_id,counts,mean,1.0,sum(counts),0,0,1_700_000_000_000,1_700_000_060_000)

def reference_execution_policy()->ExecutionDriftPolicy:
    return ExecutionDriftPolicy("execution-drift-v1",20,.05,.15,.01,2.0,5.0,250000,1000000)
