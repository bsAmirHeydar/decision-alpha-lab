from __future__ import annotations
from .contracts import CompileEvidence, GateResult, QualificationPolicy
from .enums import EvidenceStatus, GateName


def evaluate_compile(evidence: CompileEvidence, policy: QualificationPolicy, evaluated_at_ms: int) -> GateResult:
    by_target = {item.target: item for item in evidence.targets}
    reasons = []
    for target in policy.required_compile_targets:
        result = by_target.get(target)
        if result is None:
            reasons.append(f"missing_compile_target:{target}")
            continue
        if not result.passed:
            reasons.append(f"compile_failed:{target}")
        if result.warnings > policy.max_compile_warnings:
            reasons.append(f"compile_warning_budget:{target}")
    if tuple(sorted(evidence.required_targets)) != tuple(sorted(policy.required_compile_targets)):
        reasons.append("compile_policy_contract_mismatch")
    if evidence.warnings_allowed != policy.max_compile_warnings:
        reasons.append("compile_warning_policy_mismatch")
    return GateResult(GateName.METAEDITOR_COMPILE, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (evidence.evidence_hash,), evaluated_at_ms)
