"""Explicit abstention rules. A high-quality decision engine must know when not to decide."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .contracts import CandidateScore


@dataclass(frozen=True, slots=True)
class AbstentionPolicy:
    minimum_probability: float = 0.5
    minimum_expected_r: float = 0.0
    maximum_uncertainty: float | None = None
    minimum_score_margin: float = 0.0
    required_context_keys: tuple[str, ...] = ()

    def evaluate(
        self,
        scores: Sequence[CandidateScore],
        context: Mapping[str, object],
    ) -> tuple[bool, tuple[str, ...]]:
        reasons: list[str] = []
        missing = [name for name in self.required_context_keys if context.get(name) is None]
        if missing:
            reasons.append("missing_required_context:" + ",".join(sorted(missing)))
        if not scores:
            reasons.append("no_candidate_scores")
            return True, tuple(reasons)
        ranked = sorted(scores, key=lambda item: item.utility, reverse=True)
        best = ranked[0]
        if best.probability_positive < self.minimum_probability:
            reasons.append("probability_below_threshold")
        if best.expected_net_r < self.minimum_expected_r:
            reasons.append("expected_r_below_threshold")
        if self.maximum_uncertainty is not None and best.uncertainty is not None:
            if best.uncertainty > self.maximum_uncertainty:
                reasons.append("uncertainty_above_threshold")
        if len(ranked) > 1 and best.utility - ranked[1].utility < self.minimum_score_margin:
            reasons.append("insufficient_candidate_margin")
        return bool(reasons), tuple(reasons)
