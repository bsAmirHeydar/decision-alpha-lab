from __future__ import annotations
from .contracts import GateResult, ProspectiveStageEvidence, QualificationPolicy
from .enums import EvidenceStatus, GateName, ReleaseStage


_STAGE_POLICY = {
    ReleaseStage.PAPER: (GateName.PAPER, "min_paper_sessions", "min_paper_events", None),
    ReleaseStage.SHADOW: (GateName.SHADOW, "min_shadow_sessions", "min_shadow_events", None),
    ReleaseStage.MICRO_LIVE: (GateName.MICRO_LIVE, "min_micro_live_sessions", "min_micro_live_events", "max_micro_live_risk_units"),
    ReleaseStage.LIMITED_LIVE: (GateName.LIMITED_LIVE, "min_limited_live_sessions", "min_limited_live_events", "max_limited_live_risk_units"),
    ReleaseStage.PRODUCTION: (GateName.PRODUCTION, "min_production_sessions", "min_production_events", "max_production_risk_units"),
}


def evaluate_stage(evidence: ProspectiveStageEvidence, policy: QualificationPolicy, evaluated_at_ms: int) -> GateResult:
    try:
        gate, session_field, event_field, risk_field = _STAGE_POLICY[evidence.stage]
    except KeyError as exc:
        raise ValueError("stage evidence must be paper, shadow, micro_live, limited_live, or production") from exc
    min_sessions = getattr(policy, session_field)
    min_events = getattr(policy, event_field)
    reasons = []
    if evidence.end_ms > evaluated_at_ms:
        reasons.append("prospective_evidence_from_future")
    if evidence.sessions < min_sessions:
        reasons.append("prospective_sessions_below_minimum")
    if evidence.decision_events < min_events:
        reasons.append("prospective_events_below_minimum")
    if evidence.reconciliation_mismatches:
        reasons.append("prospective_reconciliation_mismatch")
    if evidence.duplicate_actions:
        reasons.append("prospective_duplicate_action")
    if evidence.critical_incidents:
        reasons.append("prospective_critical_incident")
    reject_rate = evidence.broker_rejections / max(evidence.order_intents, 1)
    if reject_rate > policy.max_broker_reject_rate:
        reasons.append("broker_reject_rate")
    if risk_field is not None:
        if evidence.max_realized_risk_units > getattr(policy, risk_field):
            reasons.append(f"{evidence.stage.value}_risk_budget")
        if policy.require_human_approval and not evidence.human_approval_id:
            reasons.append(f"{evidence.stage.value}_human_approval_missing")
    return GateResult(gate, EvidenceStatus.FAIL if reasons else EvidenceStatus.PASS, tuple(reasons), (evidence.evidence_hash,), evaluated_at_ms)
