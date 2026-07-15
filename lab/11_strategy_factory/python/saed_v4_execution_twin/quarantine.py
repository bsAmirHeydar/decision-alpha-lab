from __future__ import annotations
from .canonical import content_hash, stable_id


def quarantine_record(source_ref: str, source_hash: str, reason_code: str, detail: str) -> dict:
    payload = {"phase": "SAED_V4_09", "source_ref": source_ref, "source_hash": source_hash, "reason_code": reason_code, "detail": detail, "recovery_authority": False}
    payload["quarantine_id"] = stable_id("exectwinquarantine", payload); payload["quarantine_hash"] = content_hash(payload)
    return payload
