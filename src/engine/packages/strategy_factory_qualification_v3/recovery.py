from __future__ import annotations
from .contracts import GateResult, QualificationPolicy, RecoveryReport, RollbackDrillReport
from .enums import EvidenceStatus, GateName


def evaluate_recovery(report: RecoveryReport, policy: QualificationPolicy, evaluated_at_ms: int) -> GateResult:
    reasons = []
    checks = {
        "reservation_ledger_mismatch": report.reservation_ledger_hash != report.observed_ledger_hash,
        "duplicate_action": report.duplicate_action_count > 0,
        "unreserved_action": report.unreserved_action_count > 0,
        "state_divergence": report.state_divergence_count > 0,
        "rto_budget": report.rto_seconds > policy.max_recovery_seconds,
        "rpo_budget": report.rpo_seconds > policy.max_rpo_seconds,
        "kill_switch_unverified": not report.kill_switch_verified,
        "rollback_unverified": not report.rollback_verified,
    }
    reasons.extend(code for code, failed in checks.items() if failed)
    return GateResult(GateName.RECOVERY, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (report.report_hash,), evaluated_at_ms)


def evaluate_rollback(report: RollbackDrillReport, evaluated_at_ms: int) -> GateResult:
    reasons = []
    if report.duration_seconds > report.max_allowed_seconds:
        reasons.append("rollback_time_budget")
    if not report.orders_blocked_during_transition:
        reasons.append("orders_not_blocked_during_rollback")
    if not report.state_reconciled:
        reasons.append("rollback_state_not_reconciled")
    if not report.old_generation_restored:
        reasons.append("old_generation_not_restored")
    return GateResult(GateName.ROLLBACK, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (report.evidence_hash,), evaluated_at_ms)
