"""UCE-I10 to UCE-I11 candidate admission boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import canonical_sha256
from .contracts import BudgetPolicy, CandidateAdmission
from .enums import AdmissionDecision
from .errors import ExperimentError


@dataclass(frozen=True, slots=True)
class AdmissionSet:
    admitted: tuple[CandidateAdmission, ...]
    rejected: tuple[CandidateAdmission, ...]
    warnings: tuple[str, ...]
    evidence_hash: str


def partition_candidates(
    candidates: Iterable[CandidateAdmission],
    budget: BudgetPolicy,
    *,
    require_baseline: bool = True,
) -> AdmissionSet:
    ordered = tuple(sorted(candidates, key=lambda item: (not item.baseline, item.key)))
    if not ordered:
        raise ExperimentError("empty_candidate_set", "at least one candidate is required")
    if len({candidate.key for candidate in ordered}) != len(ordered):
        raise ExperimentError("duplicate_candidate_key", "candidate keys must be unique")

    admitted = tuple(candidate for candidate in ordered if candidate.schedulable)
    rejected = tuple(candidate for candidate in ordered if candidate.decision is AdmissionDecision.REJECT)
    warnings: list[str] = []

    if require_baseline and not any(candidate.baseline for candidate in admitted):
        raise ExperimentError(
            "admitted_baseline_missing",
            "baseline-first scheduling requires at least one admitted baseline",
        )
    if len(admitted) > budget.max_candidates:
        raise ExperimentError(
            "candidate_budget_exceeded",
            "admitted candidate count exceeds budget",
            {"admitted": len(admitted), "max_candidates": budget.max_candidates},
        )
    if not admitted:
        raise ExperimentError("no_schedulable_candidate", "all candidates were rejected")

    for candidate in admitted:
        if candidate.decision is AdmissionDecision.WARN:
            warnings.append(f"candidate_warn:{candidate.key}")
        if candidate.requires_gpu and budget.gpu_slots < 1:
            raise ExperimentError(
                "gpu_candidate_without_budget",
                "admitted GPU candidate cannot be scheduled without GPU slots",
                {"candidate": candidate.key},
            )
        if candidate.estimated_memory_mb > budget.max_memory_mb:
            raise ExperimentError(
                "candidate_memory_exceeds_budget",
                "candidate memory estimate exceeds hard budget",
                {"candidate": candidate.key, "required": candidate.estimated_memory_mb},
            )

    payload = {
        "admitted": [candidate.admission_hash for candidate in admitted],
        "rejected": [candidate.admission_hash for candidate in rejected],
        "warnings": warnings,
        "budget_hash": budget.policy_hash,
    }
    return AdmissionSet(admitted, rejected, tuple(warnings), canonical_sha256(payload))
