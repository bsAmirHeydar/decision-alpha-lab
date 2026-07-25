"""Objective freeze, baseline obligations, and objective-change detection."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .canonical import content_hash
from .enums import DecisionStatus, ReasonCode
from .models import ObjectiveDefinition


MANDATORY_BASELINES = frozenset({
    "skip_all",
    "fixed_approved_treatment",
    "manual_policy",
    "regularized_linear_or_survival",
    "calibrated_tree_or_ranker",
    "complexity_matched_ablation",
})


@dataclass(frozen=True)
class ObjectiveEvaluation:
    status: DecisionStatus
    reasons: tuple[ReasonCode, ...]
    details: tuple[str, ...]


def objective_hash(objective: ObjectiveDefinition) -> str:
    return content_hash(objective.to_dict())


def validate_baselines(baselines: Iterable[str]) -> ObjectiveEvaluation:
    supplied = frozenset(baselines)
    missing = sorted(MANDATORY_BASELINES - supplied)
    if missing:
        return ObjectiveEvaluation(
            DecisionStatus.REJECT,
            (ReasonCode.BASELINE_SET_INCOMPLETE,),
            (f"missing mandatory baselines: {missing}",),
        )
    return ObjectiveEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), ())


def detect_objective_change(current: ObjectiveDefinition, proposed: ObjectiveDefinition) -> ObjectiveEvaluation:
    if objective_hash(current) == objective_hash(proposed):
        return ObjectiveEvaluation(DecisionStatus.ALLOW, (ReasonCode.OK,), ())
    return ObjectiveEvaluation(
        DecisionStatus.REQUIRE_REVIEW,
        (ReasonCode.OBJECTIVE_CHANGE_REQUIRES_AMENDMENT,),
        ("objective definition changed and requires a non-retroactive constitutional amendment",),
    )
