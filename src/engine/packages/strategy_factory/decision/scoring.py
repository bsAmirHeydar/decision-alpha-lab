"""Candidate utility scoring and deterministic ranking."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .contracts import CandidateScore
from ..contracts import TradeCandidate


@dataclass(frozen=True, slots=True)
class UtilityWeights:
    expected_r: float = 1.0
    probability_positive: float = 0.0
    probability_target: float = 0.0
    expected_mfe: float = 0.0
    expected_mae_penalty: float = 0.0
    uncertainty_penalty: float = 0.0
    cost_penalty: float = 0.0


def score_candidates(
    candidates: Sequence[TradeCandidate],
    outputs_by_candidate: Mapping[str, Mapping[str, float]],
    *,
    weights: UtilityWeights = UtilityWeights(),
) -> tuple[CandidateScore, ...]:
    scored: list[CandidateScore] = []
    for candidate in candidates:
        raw = outputs_by_candidate.get(candidate.candidate_id, {})
        expected_r = float(raw.get("expected_net_r", 0.0))
        probability_positive = float(raw.get("probability_positive", 0.5))
        probability_target = raw.get("probability_target")
        expected_mfe = raw.get("expected_mfe_r")
        expected_mae = raw.get("expected_mae_r")
        uncertainty = raw.get("uncertainty")
        estimated_cost = float(raw.get("estimated_cost_r", 0.0))
        utility = (
            weights.expected_r * expected_r
            + weights.probability_positive * probability_positive
            + weights.probability_target * float(probability_target or 0.0)
            + weights.expected_mfe * float(expected_mfe or 0.0)
            - weights.expected_mae_penalty * abs(float(expected_mae or 0.0))
            - weights.uncertainty_penalty * float(uncertainty or 0.0)
            - weights.cost_penalty * estimated_cost
        )
        scored.append(
            CandidateScore(
                candidate_id=candidate.candidate_id,
                expected_net_r=expected_r,
                probability_positive=probability_positive,
                probability_target=None if probability_target is None else float(probability_target),
                expected_mfe_r=None if expected_mfe is None else float(expected_mfe),
                expected_mae_r=None if expected_mae is None else float(expected_mae),
                uncertainty=None if uncertainty is None else float(uncertainty),
                utility=float(utility),
                model_id=str(raw.get("model_id", "")),
                model_version=str(raw.get("model_version", "")),
            )
        )
    return tuple(sorted(scored, key=lambda item: (-item.utility, item.candidate_id)))
