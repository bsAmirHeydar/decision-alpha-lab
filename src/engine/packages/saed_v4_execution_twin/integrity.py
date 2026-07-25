from __future__ import annotations
from .canonical import content_hash, stable_id, merkle_root


def build_integrity_receipt(twin: dict) -> dict:
    hashes = [r["twin_row_hash"] for r in sorted(twin["rows"], key=lambda r: (r["source_row_id"], r["scenario_id"]))]
    payload = {
        "twin_id": twin["twin_id"], "twin_hash": twin["twin_hash"], "source_cube_hash": twin["source_cube_hash"],
        "source_handoff_hash": twin["source_handoff_hash"], "profile_hash": twin["profile_hash"], "row_merkle_root": merkle_root(hashes),
        "twin_row_count": twin["twin_row_count"], "complete_exposure": twin["complete_exposure"],
        "shadow_replacement": twin["shadow_replacement"], "selection_authority": twin["authority"]["select_treatment"],
        "execution_authority": twin["authority"]["send_order"], "synthetic_watermark": twin["synthetic_watermark"],
    }
    payload["receipt_id"] = stable_id("exectwinintegrity", payload); payload["receipt_hash"] = content_hash(payload)
    return payload
