"""Truthful classification of static versus actual external evidence."""
from __future__ import annotations
from dataclasses import dataclass
from .enums import DecisionStatus, ReasonCode

@dataclass(frozen=True)
class ExternalEvidenceClaim:
    claim_id: str
    evidence_class: str
    environment: str
    artifact_hashes: tuple[str, ...]
    actual_execution_performed: bool
    limitations: tuple[str, ...]

@dataclass(frozen=True)
class ExternalEvidenceEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]

def evaluate_external_claim(claim: ExternalEvidenceClaim) -> ExternalEvidenceEvaluation:
    if claim.evidence_class == "static" and claim.actual_execution_performed:
        return ExternalEvidenceEvaluation(DecisionStatus.REJECT,(ReasonCode.EXTERNAL_EVIDENCE_MISCLASSIFIED,),("static evidence cannot assert actual execution",))
    if claim.evidence_class == "actual" and not claim.actual_execution_performed:
        return ExternalEvidenceEvaluation(DecisionStatus.REJECT,(ReasonCode.EXTERNAL_EVIDENCE_MISCLASSIFIED,),("actual evidence requires actual external execution",))
    if not claim.artifact_hashes or any(len(x)!=64 for x in claim.artifact_hashes):
        return ExternalEvidenceEvaluation(DecisionStatus.REJECT,(ReasonCode.INVALID_SCHEMA,),("external evidence requires valid artifact hashes",))
    if claim.evidence_class not in {"static","actual"}:
        return ExternalEvidenceEvaluation(DecisionStatus.REJECT,(ReasonCode.INVALID_SCHEMA,),("unknown external evidence class",))
    return ExternalEvidenceEvaluation(DecisionStatus.ALLOW,(ReasonCode.OK,),())
