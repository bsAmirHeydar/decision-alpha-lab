from __future__ import annotations
from typing import Iterable, Optional

from .chaos import evaluate_chaos
from .compile_evidence import evaluate_compile
from .contracts import (
    ChaosReport,
    CompileEvidence,
    DifferentialReport,
    EnvironmentFingerprint,
    GateResult,
    ProspectiveStageEvidence,
    QualificationPolicy,
    QualificationReport,
    RecoveryReport,
    RollbackDrillReport,
    SecurityReport,
    SoakReport,
)
from .differential import evaluate_differential
from .enums import EvidenceStatus, GateName, QualificationDecision, ReleaseStage
from .recovery import evaluate_recovery, evaluate_rollback
from .security import evaluate_security
from .soak import evaluate_soak
from .staging import evaluate_stage

_STAGE_ORDER = {
    ReleaseStage.PAPER: 1,
    ReleaseStage.SHADOW: 2,
    ReleaseStage.MICRO_LIVE: 3,
    ReleaseStage.LIMITED_LIVE: 4,
    ReleaseStage.PRODUCTION: 5,
}


def _pending(gate: GateName, reason: str, evaluated_at_ms: int) -> GateResult:
    return GateResult(gate, EvidenceStatus.PENDING, (reason,), (), evaluated_at_ms)


def _claim_gate(
    gate: GateName,
    passed: bool,
    evidence_hash: str,
    fail_reason: str,
    missing_hash_reason: str,
    evaluated_at_ms: int,
) -> GateResult:
    if not passed:
        return GateResult(gate, EvidenceStatus.FAIL, (fail_reason,), (), evaluated_at_ms)
    if not evidence_hash:
        return GateResult(gate, EvidenceStatus.FAIL, (missing_hash_reason,), (), evaluated_at_ms)
    return GateResult(gate, EvidenceStatus.PASS, (), (evidence_hash,), evaluated_at_ms)


def _environment_reason(actual: str, expected: str, prefix: str) -> tuple[str, ...]:
    return () if actual == expected else (f"{prefix}_environment_mismatch",)


def _append_reasons(gate: GateResult, extra: tuple[str, ...]) -> GateResult:
    if not extra:
        return gate
    reasons = tuple(sorted(set(gate.reason_codes + extra)))
    return GateResult(gate.gate, EvidenceStatus.FAIL, reasons, gate.evidence_hashes, gate.evaluated_at_ms)


def qualify(
    *,
    policy: QualificationPolicy,
    environment: EnvironmentFingerprint,
    source_commit: str,
    evaluated_at_ms: int,
    requested_stage: ReleaseStage = ReleaseStage.MICRO_LIVE,
    compile_evidence: Optional[CompileEvidence] = None,
    parity_report: Optional[DifferentialReport] = None,
    tester_report: Optional[DifferentialReport] = None,
    soak_report: Optional[SoakReport] = None,
    chaos_report: Optional[ChaosReport] = None,
    recovery_report: Optional[RecoveryReport] = None,
    security_report: Optional[SecurityReport] = None,
    paper_evidence: Optional[ProspectiveStageEvidence] = None,
    shadow_evidence: Optional[ProspectiveStageEvidence] = None,
    micro_live_evidence: Optional[ProspectiveStageEvidence] = None,
    limited_live_evidence: Optional[ProspectiveStageEvidence] = None,
    production_evidence: Optional[ProspectiveStageEvidence] = None,
    rollback_report: Optional[RollbackDrillReport] = None,
    source_integrity_passed: bool = False,
    source_integrity_evidence_hash: str = "",
    broker_reconciliation_passed: bool = False,
    broker_reconciliation_evidence_hash: str = "",
    human_approval_id: str = "",
    human_approval_evidence_hash: str = "",
    limitations: Iterable[str] = (),
) -> QualificationReport:
    if requested_stage not in _STAGE_ORDER:
        raise ValueError("requested_stage must be paper, shadow, micro_live, limited_live, or production")
    env_hash = environment.fingerprint_hash
    gates: list[GateResult] = [
        _claim_gate(
            GateName.SOURCE_INTEGRITY,
            source_integrity_passed,
            source_integrity_evidence_hash,
            "source_integrity_unverified",
            "source_integrity_evidence_hash_missing",
            evaluated_at_ms,
        )
    ]

    if compile_evidence:
        gate = evaluate_compile(compile_evidence, policy, evaluated_at_ms)
        extra = _environment_reason(compile_evidence.environment_hash, env_hash, "compile")
        if compile_evidence.captured_at_ms > evaluated_at_ms:
            extra += ("compile_evidence_from_future",)
        gates.append(_append_reasons(gate, extra))
    else:
        gates.append(_pending(GateName.METAEDITOR_COMPILE, "metaeditor_compile_evidence_missing", evaluated_at_ms))

    if parity_report:
        gates.append(evaluate_differential(parity_report, policy, evaluated_at_ms, GateName.CROSS_LANGUAGE_PARITY))
    else:
        gates.append(_pending(GateName.CROSS_LANGUAGE_PARITY, "cross_language_parity_missing", evaluated_at_ms))
    if tester_report:
        gates.append(evaluate_differential(tester_report, policy, evaluated_at_ms, GateName.TESTER_DIFFERENTIAL))
    else:
        gates.append(_pending(GateName.TESTER_DIFFERENTIAL, "tester_differential_missing", evaluated_at_ms))

    if soak_report:
        gates.append(_append_reasons(evaluate_soak(soak_report, policy, evaluated_at_ms), _environment_reason(soak_report.environment_hash, env_hash, "soak")))
    else:
        gates.append(_pending(GateName.SOAK, "soak_evidence_missing", evaluated_at_ms))
    if chaos_report:
        gates.append(_append_reasons(evaluate_chaos(chaos_report, policy, evaluated_at_ms), _environment_reason(chaos_report.environment_hash, env_hash, "chaos")))
    else:
        gates.append(_pending(GateName.CHAOS, "chaos_evidence_missing", evaluated_at_ms))
    if recovery_report:
        gates.append(_append_reasons(evaluate_recovery(recovery_report, policy, evaluated_at_ms), _environment_reason(recovery_report.environment_hash, env_hash, "recovery")))
    else:
        gates.append(_pending(GateName.RECOVERY, "recovery_evidence_missing", evaluated_at_ms))

    gates.append(
        _claim_gate(
            GateName.BROKER_RECONCILIATION,
            broker_reconciliation_passed,
            broker_reconciliation_evidence_hash,
            "broker_reconciliation_failed_or_pending",
            "broker_reconciliation_evidence_hash_missing",
            evaluated_at_ms,
        )
    )
    gates.append(evaluate_security(security_report, policy, evaluated_at_ms) if security_report else _pending(GateName.SECURITY, "security_evidence_missing", evaluated_at_ms))
    gates.append(evaluate_rollback(rollback_report, evaluated_at_ms) if rollback_report else _pending(GateName.ROLLBACK, "rollback_drill_missing", evaluated_at_ms))

    stage_evidence = {
        ReleaseStage.PAPER: paper_evidence,
        ReleaseStage.SHADOW: shadow_evidence,
        ReleaseStage.MICRO_LIVE: micro_live_evidence,
        ReleaseStage.LIMITED_LIVE: limited_live_evidence,
        ReleaseStage.PRODUCTION: production_evidence,
    }
    stage_gates = {
        ReleaseStage.PAPER: GateName.PAPER,
        ReleaseStage.SHADOW: GateName.SHADOW,
        ReleaseStage.MICRO_LIVE: GateName.MICRO_LIVE,
        ReleaseStage.LIMITED_LIVE: GateName.LIMITED_LIVE,
        ReleaseStage.PRODUCTION: GateName.PRODUCTION,
    }
    for stage, order in _STAGE_ORDER.items():
        if order > _STAGE_ORDER[requested_stage]:
            continue
        evidence = stage_evidence[stage]
        if evidence:
            gate = evaluate_stage(evidence, policy, evaluated_at_ms)
            gates.append(_append_reasons(gate, _environment_reason(evidence.environment_hash, env_hash, stage.value)))
        else:
            gates.append(_pending(stage_gates[stage], f"{stage.value}_evidence_missing", evaluated_at_ms))

    live_requested = _STAGE_ORDER[requested_stage] >= _STAGE_ORDER[ReleaseStage.MICRO_LIVE]
    approval_required = policy.require_human_approval and live_requested
    if approval_required:
        approval_passed = bool(human_approval_id)
        gates.append(
            _claim_gate(
                GateName.HUMAN_APPROVAL,
                approval_passed,
                human_approval_evidence_hash,
                "human_approval_missing",
                "human_approval_evidence_hash_missing",
                evaluated_at_ms,
            )
        )
    else:
        gates.append(GateResult(GateName.HUMAN_APPROVAL, EvidenceStatus.NOT_APPLICABLE, (), (), evaluated_at_ms))

    blockers = tuple(sorted({reason for gate in gates if gate.status in (EvidenceStatus.FAIL, EvidenceStatus.PENDING) for reason in gate.reason_codes}))
    hard_fail = any(gate.status is EvidenceStatus.FAIL for gate in gates)
    unresolved = any(gate.status is EvidenceStatus.PENDING for gate in gates)
    if not hard_fail and not unresolved:
        decision = QualificationDecision.QUALIFIED
        maximum_stage = requested_stage
        activation_allowed = _STAGE_ORDER[requested_stage] >= _STAGE_ORDER[ReleaseStage.MICRO_LIVE]
        risk_caps = {
            ReleaseStage.PAPER: 0.0,
            ReleaseStage.SHADOW: 0.0,
            ReleaseStage.MICRO_LIVE: policy.max_micro_live_risk_units,
            ReleaseStage.LIMITED_LIVE: policy.max_limited_live_risk_units,
            ReleaseStage.PRODUCTION: policy.max_production_risk_units,
        }
        max_authorized_risk_units = risk_caps[requested_stage] if activation_allowed else 0.0
    elif hard_fail:
        decision = QualificationDecision.BLOCKED
        maximum_stage = ReleaseStage.BLOCKED
        activation_allowed = False
        max_authorized_risk_units = 0.0
    else:
        decision = QualificationDecision.HOLD
        maximum_stage = ReleaseStage.SHADOW
        activation_allowed = False
        max_authorized_risk_units = 0.0
    return QualificationReport(
        report_id=f"qualification:{source_commit}:{evaluated_at_ms}:{requested_stage.value}",
        schema_version="1.0.0",
        policy_hash=policy.policy_hash,
        environment_hash=env_hash,
        source_commit=source_commit,
        evaluated_at_ms=evaluated_at_ms,
        gates=tuple(gates),
        decision=decision,
        activation_allowed=activation_allowed,
        maximum_stage=maximum_stage,
        max_authorized_risk_units=max_authorized_risk_units,
        blocking_reasons=blockers,
        limitations=tuple(sorted(set(limitations))),
    )
