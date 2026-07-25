from __future__ import annotations

from .canonical import seal, stable_id


def boundary() -> dict:
    authority = {
        "decision": False,
        "promotion": False,
        "runtime": False,
        "risk_allocation": False,
        "execution": False,
        "order_submission": False,
        "production": False,
        "online_learning": False,
    }
    payload = {
        "phase": "SAED_V4_25",
        "authority": authority,
        "research_only": True,
        "safe_fallback": "scratch_baseline_or_skip",
        "ucee_authority_preserved": True,
        "central_engine_mutation": False,
        "network_access": False,
        "broker_credentials_present": False,
        "signing_material_present": False,
    }
    payload["boundary_id"] = stable_id("authority_boundary", payload)
    return seal(payload, "boundary_hash")
