import json
from pathlib import Path

def test_schemas_are_json_objects():
    root=Path(__file__).resolve().parents[2]/"schemas/v1"
    names=("exp0017_adapter_config","exp0017_legacy_candidate","exp0017_mapping_record","exp0017_differential_report","anatomy_integration_manifest","integration_stage_evidence","pilot_replay_manifest","integration_telemetry","migration_wave_plan")
    for name in names:
        data=json.loads((root/f"{name}.schema.json").read_text())
        assert data["type"]=="object" and data["$schema"].endswith("2020-12/schema")
