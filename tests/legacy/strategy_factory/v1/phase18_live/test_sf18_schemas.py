import json
from pathlib import Path

def test_phase18_schemas_are_closed_objects():
    root=Path(__file__).resolve().parents[2]/"schemas"/"v1"
    names=["micro_live_release","live_authorization","live_safety_policy","account_guard_snapshot",
      "normalized_broker_request","broker_check_result","broker_send_result","circuit_breaker_state",
      "kill_switch_state","live_decision_record","live_transaction_record","live_execution_report","live_run_manifest"]
    for name in names:
        raw=json.loads((root/f"{name}.schema.json").read_text())
        assert raw["type"]=="object" and raw["additionalProperties"] is False
