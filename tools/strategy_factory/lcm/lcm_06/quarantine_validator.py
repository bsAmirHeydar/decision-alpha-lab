from __future__ import annotations

from .canonical import digest_object

REQUIRED = (
    "source_preserved",
    "source_manifest_present",
    "source_hash_present",
    "replacement_mapping_present",
    "parity_report_present",
    "rollback_present",
    "active_consumer_count_zero",
)


def validate(record):
    missing = [key for key in REQUIRED if record.get(key) is not True]
    if not isinstance(record.get("quarantine_record_id"), str) or not record.get("quarantine_record_id"):
        missing.append("quarantine_record_id")
    out = {
        "schema_version": "1.0.0",
        "quarantine_record_id": record.get("quarantine_record_id"),
        "eligible": not missing,
        "missing_requirements": sorted(set(missing)),
        "source_move_performed": False,
        "source_delete_performed": False,
        "automatic_quarantine_allowed": False,
        "reason_code": "QUARANTINE_READY_HUMAN_EXECUTION_REQUIRED" if not missing else "QUARANTINE_EVIDENCE_INCOMPLETE",
        "validation_digest": None,
    }
    out["validation_digest"] = digest_object(out, "validation_digest")
    return out
