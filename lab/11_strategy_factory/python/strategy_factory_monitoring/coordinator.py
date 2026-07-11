from __future__ import annotations
from .alerts import AlertEngine
from .drift import evaluate_drift,evaluate_execution_drift
from .enums import Severity
from .hashing import stable_id
from .latency import FixedLatencyHistogram
from .lifecycle import build_health,recommend
from .models import (AlertPolicy,DashboardSpec,DriftBaseline,DriftObservation,DriftResult,DriftThresholdPolicy,ExecutionDriftObservation,ExecutionDriftPolicy,ExecutionDriftResult,LatencySloPolicy,MonitoringReport,MonitoringRunManifest,TelemetryEvent,TelemetrySchemaManifest)
from .ring import TelemetryRing

class MonitoringCoordinator:
    def __init__(self,manifest:MonitoringRunManifest,schema:TelemetrySchemaManifest,dashboard:DashboardSpec,latency_policies:tuple[LatencySloPolicy,...],alert_policies:tuple[AlertPolicy,...]):
        if manifest.telemetry_manifest_id!=schema.manifest_id:raise ValueError("telemetry manifest lineage mismatch")
        if manifest.dashboard_id!=dashboard.dashboard_id:raise ValueError("dashboard lineage mismatch")
        self.manifest=manifest;self.schema=schema;self.dashboard=dashboard;self.entries=schema.by_name()
        self.ring=TelemetryRing(manifest.ring_capacity);self.latency={p.stage:FixedLatencyHistogram(p) for p in latency_policies};self.alerts=AlertEngine(alert_policies)
        self.alert_events=[];self.drift_results:list[DriftResult]=[];self.execution_results:list[ExecutionDriftResult]=[];self.schema_rejections=0;self.extra_reasons=[]
    def ingest(self,event:TelemetryEvent)->bool:
        entry=self.entries.get(event.metric_name)
        if entry is None or event.schema_id!=entry.schema_id or event.run_id!=self.manifest.run_id or event.generation_id!=self.manifest.generation_id:
            self.schema_rejections+=1;return False
        if entry.lower_bound is not None and event.value<entry.lower_bound:self.schema_rejections+=1;return False
        if entry.upper_bound is not None and event.value>entry.upper_bound:self.schema_rejections+=1;return False
        if not self.ring.append(event):return False
        if event.metric_name.startswith("latency."):
            stage=event.metric_name.removeprefix("latency.").removesuffix("_us")
            histogram=self.latency.get(stage)
            if histogram:histogram.observe(int(event.value))
        self.alert_events.extend(self.alerts.observe(event.metric_name,event.value,event.known_time_ms,event.correlation_id))
        return True
    def evaluate_distribution(self,baseline:DriftBaseline,observation:DriftObservation,policy:DriftThresholdPolicy)->DriftResult:
        result=evaluate_drift(baseline,observation,policy);self.drift_results.append(result)
        metric=f"drift.{result.kind.value.lower()}.psi"
        self.alert_events.extend(self.alerts.observe(metric,result.psi,observation.window_end_ms,result.observation_id))
        return result
    def evaluate_execution(self,observation:ExecutionDriftObservation,policy:ExecutionDriftPolicy)->ExecutionDriftResult:
        result=evaluate_execution_drift(observation,policy);self.execution_results.append(result)
        self.alert_events.extend(self.alerts.observe("drift.execution.reject_rate",result.reject_rate,observation.window_end_ms,result.observation_id))
        if result.severity==Severity.CRITICAL and (observation.mismatch_count>0 or observation.missing_transaction_count>0):
            self.extra_reasons.append("RECONCILIATION_MISMATCH" if observation.mismatch_count else "MISSING_LIVE_TRANSACTION")
        return result
    def add_integrity_failure(self,reason:str)->None:
        if reason not in self.extra_reasons:self.extra_reasons.append(reason)
    def report(self,known_time_ms:int)->MonitoringReport:
        latency=tuple(h.snapshot(known_time_ms) for _,h in sorted(self.latency.items()))
        reasons=list(self.extra_reasons)
        if any(x.slo_breached for x in latency):reasons.append("LATENCY_SLO_BREACH")
        if any(x.severity==Severity.CRITICAL for x in self.drift_results):reasons.append("DISTRIBUTION_DRIFT_CRITICAL")
        active=self.alerts.active()
        health=build_health(known_time_ms,active,self.ring.dropped_count,self.ring.duplicate_count,self.schema_rejections,tuple(reasons))
        evidence=tuple(x.alert_id for x in self.alert_events[-32:])+tuple(x.result_id for x in self.drift_results[-16:])+tuple(x.result_id for x in self.execution_results[-16:])
        recommendation=recommend(health,self.manifest.strategy_id,self.manifest.model_id,self.manifest.generation_id,evidence)
        report_id=stable_id("sf19-report",self.manifest.manifest_id,known_time_ms,health.snapshot_id,recommendation.recommendation_id,len(self.ring))
        return MonitoringReport(report_id,self.manifest.manifest_id,known_time_ms,health,latency,tuple(self.drift_results),tuple(self.execution_results),tuple(self.alert_events),recommendation,len(self.ring))
