"""Immutable startup-compiled execution plan."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from ..context.graph import CompiledFeatureGraph
from ..context.vector import FeatureVectorSchema
from ..decision.abstention import AbstentionPolicy
from ..decision.scoring import UtilityWeights
from ..plugins.registry import FrozenPluginRegistry
from ..runtime.latency import LatencyBudget


@dataclass(frozen=True, slots=True)
class CandidateTemplate:
    template_id: str
    entry_policy_id: str
    stop_policy_id: str
    exit_policy_id: str
    parameters: Mapping[str, Any]
    priority: int = 0


@dataclass(frozen=True, slots=True)
class CompiledStrategyPlan:
    strategy_id: str
    strategy_version: str
    plan_hash: str
    feature_graph: CompiledFeatureGraph
    feature_schemas: Mapping[str, FeatureVectorSchema]
    candidate_templates: tuple[CandidateTemplate, ...]
    plugin_registry: FrozenPluginRegistry
    model_routes: tuple[Any, ...]
    abstention_policy: AbstentionPolicy
    utility_weights: UtilityWeights
    latency_budget: LatencyBudget
    max_candidates_per_event: int
    fallback_mode: str
    metadata: Mapping[str, Any]

    def describe(self) -> Mapping[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "plan_hash": self.plan_hash,
            "feature_provider_order": [
                p.descriptor.plugin_id for p in self.feature_graph.ordered_providers
            ],
            "feature_schemas": {key: value.names for key, value in self.feature_schemas.items()},
            "candidate_templates": [template.template_id for template in self.candidate_templates],
            "max_candidates_per_event": self.max_candidates_per_event,
            "fallback_mode": self.fallback_mode,
        }
