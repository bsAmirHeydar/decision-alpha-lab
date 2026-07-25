"""Deterministic decision policy with explicit skip/abstain behavior."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Sequence

from ..contracts import (
    AnatomyEvent,
    DecisionAction,
    ModelDecision,
    TradeCandidate,
    stable_hash,
)
from .abstention import AbstentionPolicy
from .contracts import CandidateScore, DecisionEnvelope, DecisionStatus


@dataclass(frozen=True, slots=True)
class ThresholdDecisionPolicy:
    model_id: str
    model_version: str
    feature_schema_version: str
    model_artifact_hash: str
    abstention: AbstentionPolicy

    def decide(
        self,
        event: AnatomyEvent,
        candidates: Sequence[TradeCandidate],
        scores: Sequence[CandidateScore],
        context: Mapping[str, object],
        decision_time_utc: datetime,
        *,
        plan_hash: str = "",
        context_hash: str = "",
        latency_ns: Mapping[str, int] | None = None,
    ) -> DecisionEnvelope:
        abstain, reasons = self.abstention.evaluate(scores, context)
        best_score = scores[0] if scores else None
        selected = None
        if best_score is not None:
            selected = next((c for c in candidates if c.candidate_id == best_score.candidate_id), None)
        if abstain or selected is None:
            action = DecisionAction.SKIP
            status = DecisionStatus.ABSTAIN
            candidate_id = None
        else:
            action = DecisionAction.TRADE
            status = DecisionStatus.TRADE
            candidate_id = selected.candidate_id
        payload = {
            "event_id": event.event_id,
            "candidate_id": candidate_id,
            "decision_time": decision_time_utc.isoformat(),
            "model_id": self.model_id,
            "model_version": self.model_version,
            "plan_hash": plan_hash,
            "context_hash": context_hash,
        }
        model_decision = ModelDecision(
            decision_id=stable_hash(payload, prefix="dec_")[:40],
            event_id=event.event_id,
            candidate_id=candidate_id,
            model_id=self.model_id,
            model_version=self.model_version,
            decision_time_utc=decision_time_utc,
            action=action,
            predicted_probability=None if best_score is None else best_score.probability_positive,
            expected_net_r=None if best_score is None else best_score.expected_net_r,
            expected_mfe_r=None if best_score is None else best_score.expected_mfe_r,
            expected_mae_r=None if best_score is None else best_score.expected_mae_r,
            confidence_tier="abstain" if abstain else "eligible",
            feature_schema_version=self.feature_schema_version,
            model_artifact_hash=self.model_artifact_hash,
            explanations={"utility": 0.0 if best_score is None else best_score.utility},
        )
        model_decision.validate()
        return DecisionEnvelope(
            event=event,
            candidates=tuple(candidates),
            model_decision=model_decision,
            status=status,
            selected_candidate=selected if status == DecisionStatus.TRADE else None,
            scores=tuple(scores),
            created_time_utc=decision_time_utc,
            reason_codes=reasons,
            context_hash=context_hash,
            plan_hash=plan_hash,
            latency_ns=dict(latency_ns or {}),
        )
