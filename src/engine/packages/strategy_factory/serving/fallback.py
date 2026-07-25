"""Deterministic fallbacks used when model/context/runtime requirements fail."""
from __future__ import annotations

from datetime import datetime
from typing import Sequence

from ..contracts import AnatomyEvent, DecisionAction, ModelDecision, TradeCandidate, stable_hash
from ..decision.contracts import DecisionEnvelope, DecisionStatus


def abstain_envelope(
    event: AnatomyEvent,
    candidates: Sequence[TradeCandidate],
    decision_time_utc: datetime,
    *,
    reason_codes: Sequence[str],
    plan_hash: str,
    context_hash: str = "",
    latency_ns: dict[str, int] | None = None,
) -> DecisionEnvelope:
    payload = {
        "event_id": event.event_id,
        "time": decision_time_utc.isoformat(),
        "reasons": list(reason_codes),
        "plan_hash": plan_hash,
    }
    decision = ModelDecision(
        decision_id=stable_hash(payload, prefix="dec_")[:40],
        event_id=event.event_id,
        candidate_id=None,
        model_id="deterministic_fallback",
        model_version="2.0.0",
        decision_time_utc=decision_time_utc,
        action=DecisionAction.SKIP,
        predicted_probability=None,
        expected_net_r=None,
        expected_mfe_r=None,
        expected_mae_r=None,
        confidence_tier="abstain",
        feature_schema_version="fallback",
        model_artifact_hash="fallback",
        explanations={},
    )
    return DecisionEnvelope(
        event=event,
        candidates=tuple(candidates),
        model_decision=decision,
        status=DecisionStatus.ABSTAIN,
        selected_candidate=None,
        scores=(),
        created_time_utc=decision_time_utc,
        reason_codes=tuple(reason_codes),
        context_hash=context_hash,
        plan_hash=plan_hash,
        latency_ns=dict(latency_ns or {}),
    )
