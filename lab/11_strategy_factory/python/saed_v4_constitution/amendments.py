"""Non-retroactive, independently approved constitutional amendment protocol."""
from __future__ import annotations

from dataclasses import dataclass

from .canonical import parse_time
from .enums import Authority, DecisionStatus, ReasonCode
from .models import AmendmentProposal
from .review import evaluate_two_person_integrity


NON_AMENDABLE_BY_RESEARCH = frozenset({
    Authority.ORDER.value,
    Authority.BROKER.value,
    Authority.NETWORK.value,
    Authority.RISK_LIMIT_CHANGE.value,
    Authority.PROMOTION_SIGNATURE.value,
    Authority.RUNTIME_ACTIVATION.value,
    Authority.CONTEXT_TRUTH_MUTATION.value,
    Authority.EVIDENCE_ROLE_REASSIGNMENT.value,
    Authority.CONSTITUTION_SELF_AMENDMENT.value,
})


@dataclass(frozen=True)
class AmendmentEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]


class AmendmentGate:
    def evaluate(self, proposal: AmendmentProposal, active_constitution_hash: str) -> AmendmentEvaluation:
        if proposal.current_constitution_hash != active_constitution_hash:
            return AmendmentEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.LINEAGE_MISMATCH,),
                ("proposal is not based on the active constitution hash",),
            )
        if proposal.applies_to_existing_programs:
            return AmendmentEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.RETROACTIVE_AMENDMENT,),
                ("constitutional amendments cannot retroactively alter existing programs or trials",),
            )
        if parse_time(proposal.effective_from) < parse_time(proposal.known_time):
            return AmendmentEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.RETROACTIVE_AMENDMENT,),
                ("effective_from cannot precede known_time",),
            )
        if parse_time(proposal.expires_at) <= parse_time(proposal.known_time):
            return AmendmentEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.WAIVER_EXPIRED,),
                ("proposal review window has expired",),
            )
        if any(token in proposal.target_section for token in NON_AMENDABLE_BY_RESEARCH):
            return AmendmentEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.NON_WAIVABLE_RULE,),
                ("research process cannot amend hard authority prohibitions",),
            )
        review = evaluate_two_person_integrity(proposal.proposer, proposal.approvals)
        return AmendmentEvaluation(review.status, review.reasons, review.details)
