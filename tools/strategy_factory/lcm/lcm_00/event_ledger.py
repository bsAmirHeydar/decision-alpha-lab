from __future__ import annotations

from .canonical import content_id, digest_object
from .errors import IntegrityError

EVENT_TYPES = (
    "PROGRAM_CONSTITUTION_BOUND",
    "SOURCE_SCOPE_FROZEN",
    "REPOSITORY_STATE_CAPTURED",
    "OWNERSHIP_AND_AUTHORITY_RECORDED",
    "CONTENT_MANIFEST_CREATED",
    "RESTORE_REHEARSAL_COMPLETED",
    "BASELINE_VERIFIED",
    "LCM01_HANDOFF_PREPARED",
)


def build_event_ledger(events: list[dict], occurred_at: str) -> dict:
    chain: list[dict] = []
    previous = "GENESIS"
    for sequence, payload in enumerate(events, 1):
        event_type = payload["event_type"]
        if event_type not in EVENT_TYPES:
            raise IntegrityError(f"unknown event type: {event_type}")
        event = {
            "sequence": sequence,
            "event_id": content_id("LCM00EVT", {"sequence": sequence, "event_type": event_type, "payload": payload}),
            "event_type": event_type,
            "occurred_at": occurred_at,
            "previous_event_digest": previous,
            "payload": payload.get("payload", {}),
            "move_authority": False,
            "delete_authority": False,
            "semantic_change_authority": False,
            "execution_authority": False,
            "capital_authority": False,
            "event_digest": "",
        }
        event["event_digest"] = digest_object(event, "event_digest")
        previous = event["event_digest"]
        chain.append(event)
    ledger = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-00",
        "event_count": len(chain),
        "events": chain,
        "head_event_digest": previous,
        "ledger_digest": "",
    }
    ledger["ledger_digest"] = digest_object(ledger, "ledger_digest")
    return ledger


def verify_event_ledger(ledger: dict) -> None:
    previous = "GENESIS"
    for index, event in enumerate(ledger.get("events", []), 1):
        if event.get("sequence") != index:
            raise IntegrityError("event sequence mismatch")
        if event.get("previous_event_digest") != previous:
            raise IntegrityError("event chain mismatch")
        if event.get("event_digest") != digest_object(event, "event_digest"):
            raise IntegrityError("event digest mismatch")
        previous = event["event_digest"]
    if ledger.get("head_event_digest") != previous:
        raise IntegrityError("ledger head mismatch")
    if ledger.get("ledger_digest") != digest_object(ledger, "ledger_digest"):
        raise IntegrityError("ledger digest mismatch")
