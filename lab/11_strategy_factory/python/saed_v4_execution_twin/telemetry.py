from __future__ import annotations
from .canonical import content_hash, stable_id


def build_telemetry(twin: dict) -> dict:
    rows = twin["rows"]
    order_rows = [r for r in rows if r["action_class"] not in {"skip", "abstain"}]
    payload = {
        "twin_id": twin["twin_id"], "twin_hash": twin["twin_hash"], "source_row_count": twin["source_row_count"],
        "scenario_count": twin["scenario_count"], "twin_row_count": twin["twin_row_count"],
        "order_projection_count": len(order_rows), "full_fill_count": sum(r["status"] == "filled" for r in order_rows),
        "partial_fill_count": sum(r["status"] == "partially_filled" for r in order_rows), "unfilled_count": sum(r["status"] == "unfilled" for r in order_rows),
        "rejected_count": sum(r["status"] == "rejected" for r in order_rows), "broker_infeasible_count": sum(r["status"] == "broker_infeasible" for r in order_rows),
        "complete_exposure": twin["complete_exposure"], "synthetic_watermark": twin["synthetic_watermark"], "shadow_replacement": twin["shadow_replacement"],
    }
    payload["telemetry_id"] = stable_id("exectwintelemetry", payload); payload["telemetry_hash"] = content_hash(payload)
    return payload
