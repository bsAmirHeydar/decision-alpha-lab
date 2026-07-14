"""Two-person integrity and independent-review enforcement."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .enums import DecisionStatus, ReasonCode
from .models import Actor, ReviewApproval


@dataclass(frozen=True)
class ReviewEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]


def evaluate_two_person_integrity(
    proposer: Actor,
    approvals: Iterable[ReviewApproval],
    required_count: int = 2,
) -> ReviewEvaluation:
    approved = [a for a in approvals if a.decision == "approve"]
    unique_reviewers = {a.reviewer_id for a in approved}
    if proposer.actor_id in unique_reviewers:
        return ReviewEvaluation(
            DecisionStatus.REJECT,
            (ReasonCode.SELF_APPROVAL,),
            ("proposer cannot approve own proposal",),
        )
    if any(a.organization_unit == proposer.organization_unit for a in approved):
        return ReviewEvaluation(
            DecisionStatus.REJECT,
            (ReasonCode.REVIEWER_NOT_INDEPENDENT,),
            ("reviewer must be organizationally independent from proposer",),
        )
    if len(unique_reviewers) < required_count:
        return ReviewEvaluation(
            DecisionStatus.REQUIRE_REVIEW,
            (ReasonCode.MISSING_SECOND_APPROVAL,),
            (f"requires {required_count} independent approvals; found {len(unique_reviewers)}",),
        )
    if any(not a.signature_hash or len(a.signature_hash) != 64 for a in approved):
        return ReviewEvaluation(
            DecisionStatus.REJECT,
            (ReasonCode.SIGNATURE_INVALID,),
            ("all approvals require a 64-character signature hash",),
        )
    return ReviewEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), ())
