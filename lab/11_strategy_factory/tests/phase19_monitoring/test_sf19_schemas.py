from pathlib import Path
import json
from jsonschema import Draft202012Validator

def repo():return Path(__file__).resolve().parents[4]

def test_all_phase19_schemas_are_valid():
    root=repo()/"lab/11_strategy_factory/schemas/v1"
    names=("telemetry_schema_entry","telemetry_schema_manifest","telemetry_event","latency_slo_policy","latency_histogram","drift_baseline","drift_observation","drift_threshold_policy","drift_result","execution_drift_observation","execution_drift_policy","execution_drift_result","alert_policy","alert_event","health_snapshot","lifecycle_recommendation","monitoring_run_manifest","dashboard_spec","response_playbook","monitoring_report")
    for name in names:Draft202012Validator.check_schema(json.loads((root/f"{name}.schema.json").read_text()))

def test_examples_are_parseable_json():
    files=list((repo()/"lab/11_strategy_factory/examples/phase19").glob("*.json"));assert len(files)>=15
    for p in files:json.loads(p.read_text())
