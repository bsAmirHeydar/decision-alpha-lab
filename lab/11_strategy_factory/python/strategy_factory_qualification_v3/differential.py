from __future__ import annotations
from .contracts import DifferentialReport, GateResult, QualificationPolicy
from .enums import EvidenceStatus, GateName


def evaluate_differential(report: DifferentialReport, policy: QualificationPolicy, evaluated_at_ms: int, gate: GateName = GateName.CROSS_LANGUAGE_PARITY) -> GateResult:
    by_id = {case.case_id: case for case in report.cases}
    reasons = []
    if report.causal_cut_ms > evaluated_at_ms:
        reasons.append("causal_cut_after_evaluation")
    for case_id in policy.required_differential_cases:
        case = by_id.get(case_id)
        if case is None:
            reasons.append(f"missing_differential_case:{case_id}")
        elif not case.passed:
            reasons.append(f"differential_mismatch:{case_id}")
    reasons.extend(f"declared_missing_case:{case_id}" for case_id in report.missing_case_ids)
    if report.future_read_count:
        reasons.append("future_read_detected")
    if report.reordered_event_count:
        reasons.append("event_order_violation")
    return GateResult(gate, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(sorted(set(reasons))), (report.report_hash,), evaluated_at_ms)
