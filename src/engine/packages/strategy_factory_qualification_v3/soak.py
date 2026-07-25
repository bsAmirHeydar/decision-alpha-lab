from __future__ import annotations
from .contracts import GateResult, QualificationPolicy, SoakReport
from .enums import EvidenceStatus, GateName


def evaluate_soak(report: SoakReport, policy: QualificationPolicy, evaluated_at_ms: int) -> GateResult:
    reasons = []
    checks = {
        "soak_duration_below_minimum": report.duration_minutes < policy.min_soak_minutes,
        "soak_events_below_minimum": report.processed_events < policy.min_soak_events,
        "critical_error": report.critical_errors > 0,
        "unhandled_exception": report.unhandled_exceptions > 0,
        "reconciliation_mismatch": report.reconciliation_mismatches > 0,
        "duplicate_action": report.duplicate_actions > 0,
        "stale_action": report.stale_actions > 0,
        "memory_growth_budget": report.max_memory_growth_mb > policy.max_memory_growth_mb,
        "latency_budget": report.p99_latency_ms > policy.max_p99_latency_ms,
    }
    reasons.extend(code for code, failed in checks.items() if failed)
    return GateResult(GateName.SOAK, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (report.report_hash,), evaluated_at_ms)
