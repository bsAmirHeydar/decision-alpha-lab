from __future__ import annotations

from .canonical import digest_object
from .registries import DELETION_GATES


def validate(record):
    gates = record.get("gates", {})
    if not isinstance(gates, dict):
        gates = {}
    missing = [key for key in DELETION_GATES if gates.get(key) is not True]
    if not isinstance(record.get("deletion_record_id"), str) or not record.get("deletion_record_id"):
        missing.append("deletion_record_id")
    out = {
        "schema_version": "1.0.0",
        "deletion_record_id": record.get("deletion_record_id"),
        "eligible": not missing,
        "passed_gate_count": len(DELETION_GATES) - len([key for key in DELETION_GATES if key in missing]),
        "required_gate_count": len(DELETION_GATES),
        "missing_gates": sorted(set(missing)),
        "automatic_delete_allowed": False,
        "delete_performed": False,
        "reason_code": "DELETION_ELIGIBLE_HUMAN_EXECUTION_STILL_REQUIRED" if not missing else "DELETION_GATES_INCOMPLETE",
        "validation_digest": None,
    }
    out["validation_digest"] = digest_object(out, "validation_digest")
    return out
