from __future__ import annotations

from .contracts import ReconciliationReport
from .enums import EvidenceState


def reconciliation_status(report: ReconciliationReport, expected_environment_hash: str, expected_generation_hash: str, evaluated_at_ms: int, max_age_ms: int) -> tuple[EvidenceState, tuple[str, ...]]:
    reasons: list[str] = []
    if report.environment_hash != expected_environment_hash:
        reasons.append("reconciliation_environment_mismatch")
    if report.generation_hash != expected_generation_hash:
        reasons.append("reconciliation_generation_mismatch")
    if report.reconciled_at_ms > evaluated_at_ms:
        reasons.append("reconciliation_from_future")
    if evaluated_at_ms - report.reconciled_at_ms > max_age_ms:
        reasons.append("reconciliation_stale")
    if report.expected_reservation_hash != report.observed_reservation_hash:
        reasons.append("reservation_hash_mismatch")
    if report.expected_order_hash != report.observed_order_hash:
        reasons.append("order_hash_mismatch")
    if report.expected_position_hash != report.observed_position_hash:
        reasons.append("position_hash_mismatch")
    for field_name in (
        "orphan_order_count",
        "orphan_position_count",
        "missing_order_count",
        "missing_position_count",
        "duplicate_intent_count",
        "unreserved_position_count",
    ):
        if getattr(report, field_name):
            reasons.append(field_name)
    return (EvidenceState.PASS, ()) if not reasons else (EvidenceState.FAIL, tuple(sorted(set(reasons))))
