from __future__ import annotations
import argparse,json
from dataclasses import asdict
from .coordinator import MonitoringCoordinator
from .examples import *
from .hashing import canonical_json

def build_reference_report(shifted:bool=False):
    now=1_700_000_000_000;schema=reference_schema();dash=reference_dashboard(now);manifest=reference_manifest(now)
    c=MonitoringCoordinator(manifest,schema,dash,reference_latency_policies(),reference_alert_policies())
    for i,value in enumerate((400,600,800,1200,2000),1):
        e=schema.by_name()["latency.pipeline_us"]
        from .models import TelemetryEvent
        c.ingest(TelemetryEvent(e.metric_name,e.schema_id,manifest.run_id,manifest.generation_id,manifest.strategy_id,manifest.model_id,f"corr-{i}","cause",now+i,now+i,i,float(value)))
    c.evaluate_distribution(reference_baseline(),reference_observation(shifted),reference_drift_policy())
    return c.report(now+1000)

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog="strategy-factory-monitoring");p.add_argument("--shifted",action="store_true");p.add_argument("--compact",action="store_true")
    a=p.parse_args(argv);report=build_reference_report(a.shifted)
    print(canonical_json(report) if a.compact else json.dumps(asdict(report),default=lambda x:getattr(x,"value",str(x)),indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
