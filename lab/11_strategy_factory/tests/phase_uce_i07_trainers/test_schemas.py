from pathlib import Path
import json
def test_i07_schemas_closed():
 root=Path(__file__).resolve().parents[2]/'schemas'/'v3';names=['trainer_capability_descriptor','trainer_config','trainer_resource_budget','task_contract','dataset_schema','fold_definition','oof_protocol','task_orchestration_plan','prediction_lineage','prediction_record','prediction_batch','trial_ledger_entry','access_audit_record','model_state_bundle','model_artifact_manifest','model_card','trainer_telemetry','trainer_registry_snapshot','trainer_conformance_case']
 for n in names:
  o=json.loads((root/f'{n}.schema.json').read_text());assert o['additionalProperties'] is False and o['required']
