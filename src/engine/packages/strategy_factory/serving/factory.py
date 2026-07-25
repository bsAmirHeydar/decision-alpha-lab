"""Build a reference fast decision engine from a V2 specification."""
from __future__ import annotations

from typing import Any, Mapping

from ..context.engine import IncrementalContextEngine
from ..decision.policy import ThresholdDecisionPolicy
from ..optimization.compiler import compile_strategy_plan
from ..plugins.builtins import register_builtins_from_spec
from ..plugins.registry import PluginRegistry
from .candidates import CompiledCandidateFactory
from .fast_path import FastDecisionEngine


def build_reference_fast_engine(
    spec: Mapping[str, Any],
    *,
    registry: PluginRegistry | None = None,
) -> FastDecisionEngine:
    registry = registry or PluginRegistry()
    register_builtins_from_spec(spec, registry)
    plan = compile_strategy_plan(spec, registry)
    context_engine = IncrementalContextEngine(plan.feature_graph)
    candidate_factory = CompiledCandidateFactory(plan)
    first_model = spec.get("decision", {}).get("models", [{}])[0]
    policy = ThresholdDecisionPolicy(
        model_id=str(first_model.get("id", "compiled_models")),
        model_version=str(first_model.get("version", "1.0.0")),
        feature_schema_version="|".join(
            f"{key}:{schema.version}" for key, schema in sorted(plan.feature_schemas.items())
        ),
        model_artifact_hash=plan.plan_hash,
        abstention=plan.abstention_policy,
    )
    return FastDecisionEngine(plan, context_engine, candidate_factory, policy)
