from __future__ import annotations
from .canonical import content_hash, stable_id
from .integrity import build_integrity_receipt


def build_v4_10_handoff(twin: dict) -> dict:
    receipt = build_integrity_receipt(twin)
    payload = {
        "phase": "SAED_V4_09", "next_phase": "SAED_V4_10",
        "authority": {
            "read_frozen_execution_twin": True, "read_source_outcome_cube_identity": True, "read_scenario_surfaces": True,
            "build_baseline_and_manual_program": True, "mutate_execution_twin": False, "replace_shadow_or_prospective": False,
            "rank_treatments": False, "select_treatment": False, "allocate_risk": False, "activate_runtime": False, "send_order": False,
        },
        "twin_id": twin["twin_id"], "twin_hash": twin["twin_hash"], "integrity_receipt_hash": receipt["receipt_hash"],
        "source_cube_id": twin["source_cube_id"], "source_cube_hash": twin["source_cube_hash"], "profile_hash": twin["profile_hash"],
        "complete_exposure": twin["complete_exposure"], "evidence_class": twin["evidence_class"], "synthetic_watermark": twin["synthetic_watermark"],
        "limitations": [
            "V4-10 must preserve V4-09 twin identity and source row/scenario coverage.",
            "Synthetic execution stress cannot be used as positive promotion evidence.",
            "Manual and baseline programs remain non-authoritative until later UCEE admission and qualification.",
        ],
    }
    payload["handoff_id"] = stable_id("v409to10", payload); payload["handoff_hash"] = content_hash(payload)
    return payload
