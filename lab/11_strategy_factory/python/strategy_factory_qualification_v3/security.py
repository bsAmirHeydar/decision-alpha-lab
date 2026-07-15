from __future__ import annotations
from .contracts import GateResult, QualificationPolicy, SecurityReport
from .enums import EvidenceStatus, GateName


def evaluate_security(report: SecurityReport, policy: QualificationPolicy, evaluated_at_ms: int) -> GateResult:
    by_id = {item.control_id: item for item in report.controls}
    reasons = []
    if tuple(sorted(report.required_control_ids)) != tuple(sorted(policy.required_security_controls)):
        reasons.append("security_policy_contract_mismatch")
    for control_id in policy.required_security_controls:
        result = by_id.get(control_id)
        if result is None:
            reasons.append(f"missing_security_control:{control_id}")
        elif result.status is not EvidenceStatus.PASS:
            reasons.append(f"security_control_not_passed:{control_id}")
    if report.plaintext_secret_findings:
        reasons.append("plaintext_secret_finding")
    if report.unsigned_artifacts:
        reasons.append("unsigned_artifact")
    if report.hash_mismatches:
        reasons.append("artifact_hash_mismatch")
    if not report.backup_restore_verified:
        reasons.append("backup_restore_unverified")
    if not report.retention_policy_verified:
        reasons.append("retention_policy_unverified")
    return GateResult(GateName.SECURITY, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (report.report_hash,), evaluated_at_ms)
