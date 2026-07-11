import json
from pathlib import Path

def test_schemas_are_draft_2020_objects():
    root=Path(__file__).resolve().parents[2]/"schemas"/"v1"
    names=["quote_observation","paper_execution_policy","paper_order","fill_record","position_record","transaction_record",
      "observed_position","reconciliation_report","shadow_comparison","execution_telemetry","execution_report","execution_run_manifest"]
    for name in names:
        raw=json.loads((root/f"{name}.schema.json").read_text())
        assert raw["type"]=="object" and raw["additionalProperties"] is False
