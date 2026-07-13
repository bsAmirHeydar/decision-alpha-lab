import json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
SCHEMA_DIR=ROOT/'lab/11_strategy_factory/schemas/v3'
NAMES=(
'runtime_artifact_ref','runtime_feature_rule','runtime_preprocessing_contract','runtime_native_model_artifact','runtime_export_record','runtime_bundle_manifest','runtime_parity_tolerance','runtime_parity_vector','runtime_parity_observation','runtime_parity_certificate','runtime_request','runtime_decision','runtime_generation_record','runtime_activation_receipt','runtime_failure_finding','runtime_failure_report','runtime_evidence_bundle','runtime_adapter_registry','runtime_replay_manifest','runtime_restart_snapshot','runtime_latency_policy','runtime_monitoring_policy','runtime_rollback_plan','runtime_capability_manifest','runtime_handoff_bundle')
@pytest.mark.parametrize('name',NAMES)
def test_schema_is_closed_versioned_and_parseable(name):
    p=SCHEMA_DIR/f'{name}.schema.json';assert p.is_file();s=json.loads(p.read_text());assert s['$schema'].startswith('https://json-schema.org/');assert s['type']=='object';assert s['additionalProperties'] is False;assert s['properties'];assert '$id' in s
