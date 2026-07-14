"""Sunset-bound waiver protocol with a hard non-waivable core."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from .canonical import parse_time
from .enums import DecisionStatus, ReasonCode


NON_WAIVABLE_RULES = frozenset({
    "no_order_authority",
    "no_broker_authority",
    "no_network_authority",
    "no_risk_limit_expansion",
    "no_context_truth_mutation",
    "no_evidence_tampering",
    "no_autonomous_promotion",
    "no_runtime_activation",
    "no_constitution_self_amendment",
    "protected_evidence_firewall",
})


@dataclass(frozen=True)
class WaiverRequest:
    waiver_id: str
    program_id: str
    rule_id: str
    proposer_id: str
    known_time: str
    effective_from: str
    expires_at: str
    rationale: str
    compensating_controls: tuple[str, ...]
    approval_ids: tuple[str, ...]


@dataclass(frozen=True)
class WaiverEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]


class WaiverGate:
    def __init__(self, max_duration_days: int = 90) -> None:
        self.max_duration = timedelta(days=max_duration_days)

    def evaluate(self, request: WaiverRequest) -> WaiverEvaluation:
        if request.rule_id in NON_WAIVABLE_RULES:
            return WaiverEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.NON_WAIVABLE_RULE,),
                (f"{request.rule_id} is constitutionally non-waivable",),
            )
        start = parse_time(request.effective_from)
        end = parse_time(request.expires_at)
        known = parse_time(request.known_time)
        if start < known or end <= start or end - start > self.max_duration:
            return WaiverEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.WAIVER_EXPIRED,),
                ("waiver must be prospective, time-bounded, and within maximum duration",),
            )
        if len(set(request.approval_ids)) < 2:
            return WaiverEvaluation(
                DecisionStatus.REQUIRE_REVIEW,
                (ReasonCode.MISSING_SECOND_APPROVAL,),
                ("waiver requires two distinct approvals",),
            )
        if not request.compensating_controls:
            return WaiverEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.INVALID_SCHEMA,),
                ("waiver requires compensating controls",),
            )
        return WaiverEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), ())
