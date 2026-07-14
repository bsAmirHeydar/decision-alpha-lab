"""Semantic validation for frozen phase-zero research program manifests."""
from __future__ import annotations
from dataclasses import dataclass
from .enums import DecisionStatus, ReasonCode

@dataclass(frozen=True)
class ProgramEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]

def evaluate_program_manifest(manifest: dict) -> ProgramEvaluation:
    hashes=[manifest.get(k,"") for k in ("constitution_hash","objective_hash","authority_matrix_hash","evidence_policy_hash","crosswalk_hash")]
    if any(len(x)!=64 for x in hashes):
        return ProgramEvaluation(DecisionStatus.REJECT,(ReasonCode.LINEAGE_MISMATCH,),("all governing artifacts must be SHA-256 pinned",))
    owners=manifest.get("owners",{})
    if len({owners.get("primary"),owners.get("independent_validation"),owners.get("risk_owner")})<3:
        return ProgramEvaluation(DecisionStatus.REJECT,(ReasonCode.REVIEWER_NOT_INDEPENDENT,),("program, independent validation and risk ownership must be separated",))
    budgets=manifest.get("budgets",{})
    if budgets.get("hidden_submissions",0)>budgets.get("exposure_total",0):
        return ProgramEvaluation(DecisionStatus.REJECT,(ReasonCode.INVALID_SCHEMA,),("hidden submission budget cannot exceed total exposure budget",))
    if manifest.get("status") not in {"frozen","active","quarantined","retired"}:
        return ProgramEvaluation(DecisionStatus.REJECT,(ReasonCode.INVALID_SCHEMA,),("unknown program status",))
    return ProgramEvaluation(DecisionStatus.ALLOW,(ReasonCode.OK,),())
