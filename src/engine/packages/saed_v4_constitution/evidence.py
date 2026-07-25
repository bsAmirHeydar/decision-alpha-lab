"""Evidence-role firewall and external evidence classification."""
from __future__ import annotations

from dataclasses import dataclass

from .enums import DecisionStatus, EvidenceOperation, EvidenceRole, ReasonCode
from .models import EvidenceUseRequest


TRAINING_LIKE = frozenset({EvidenceOperation.TRAIN, EvidenceOperation.TUNE})
PROTECTED_ROLES = frozenset({
    EvidenceRole.LOCKED_FINAL,
    EvidenceRole.PROSPECTIVE,
    EvidenceRole.SHADOW,
    EvidenceRole.MICRO_LIVE,
    EvidenceRole.LIVE,
    EvidenceRole.EXTERNAL_ACTUAL,
})

ROLE_PERMISSIONS: dict[EvidenceRole, frozenset[EvidenceOperation]] = {
    EvidenceRole.DEVELOPMENT: frozenset({EvidenceOperation.TRAIN, EvidenceOperation.TUNE, EvidenceOperation.REPORT, EvidenceOperation.REPLAY}),
    EvidenceRole.CALIBRATION: frozenset({EvidenceOperation.CALIBRATE, EvidenceOperation.REPORT, EvidenceOperation.REPLAY}),
    EvidenceRole.SELECTION_VALIDATION: frozenset({EvidenceOperation.SELECT, EvidenceOperation.REPORT, EvidenceOperation.REPLAY}),
    EvidenceRole.LOCKED_FINAL: frozenset({EvidenceOperation.REPORT, EvidenceOperation.PROMOTE, EvidenceOperation.REPLAY}),
    EvidenceRole.PROSPECTIVE: frozenset({EvidenceOperation.REPORT, EvidenceOperation.PROMOTE, EvidenceOperation.REPLAY}),
    EvidenceRole.SHADOW: frozenset({EvidenceOperation.REPORT, EvidenceOperation.PROMOTE, EvidenceOperation.REPLAY}),
    EvidenceRole.MICRO_LIVE: frozenset({EvidenceOperation.REPORT, EvidenceOperation.PROMOTE, EvidenceOperation.REPLAY}),
    EvidenceRole.LIVE: frozenset({EvidenceOperation.REPORT, EvidenceOperation.REPLAY}),
    EvidenceRole.SYNTHETIC_STRESS: frozenset({EvidenceOperation.STRESS, EvidenceOperation.REPORT, EvidenceOperation.REPLAY}),
    EvidenceRole.EXTERNAL_STATIC: frozenset({EvidenceOperation.REPORT, EvidenceOperation.REPLAY}),
    EvidenceRole.EXTERNAL_ACTUAL: frozenset({EvidenceOperation.REPORT, EvidenceOperation.PROMOTE, EvidenceOperation.REPLAY}),
}


@dataclass(frozen=True)
class EvidenceEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]


class EvidenceFirewall:
    def evaluate(self, request: EvidenceUseRequest) -> EvidenceEvaluation:
        # Specific constitutional prohibitions are evaluated before generic role denial
        # so audit evidence records the most informative failure reason.
        if request.synthetic or request.evidence_role == EvidenceRole.SYNTHETIC_STRESS:
            if request.positive_promotion_claim or request.operation == EvidenceOperation.PROMOTE:
                return EvidenceEvaluation(
                    DecisionStatus.REJECT,
                    (ReasonCode.SYNTHETIC_POSITIVE_PROMOTION,),
                    ("synthetic evidence can falsify but cannot provide positive promotion evidence",),
                )

        allowed = ROLE_PERMISSIONS.get(request.evidence_role, frozenset())
        if request.operation not in allowed:
            reason = ReasonCode.PROTECTED_EVIDENCE_TRAINING if request.operation in TRAINING_LIKE else ReasonCode.AUTHORITY_DENIED
            return EvidenceEvaluation(
                DecisionStatus.REJECT,
                (reason,),
                (f"{request.operation.value} is not allowed for {request.evidence_role.value}",),
            )

        if request.evidence_role in PROTECTED_ROLES and request.operation in TRAINING_LIKE:
            return EvidenceEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.PROTECTED_EVIDENCE_TRAINING,),
                ("protected evidence cannot feed training or adaptive search",),
            )

        if request.evidence_role == EvidenceRole.EXTERNAL_STATIC and request.operation == EvidenceOperation.PROMOTE:
            return EvidenceEvaluation(
                DecisionStatus.REJECT,
                (ReasonCode.EXTERNAL_EVIDENCE_MISCLASSIFIED,),
                ("static evidence cannot be represented as actual external evidence",),
            )

        return EvidenceEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), ())
