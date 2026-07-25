"""Compile declarative V2 strategy specifications into immutable fast-path plans."""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from ..context.graph import compile_feature_graph
from ..context.vector import FeatureVectorSchema
from ..contracts import stable_hash
from ..decision.abstention import AbstentionPolicy
from ..decision.models import ModelRoute
from ..decision.scoring import UtilityWeights
from ..plugins.registry import PluginRegistry
from ..runtime.latency import LatencyBudget
from .plan import CandidateTemplate, CompiledStrategyPlan


class PlanCompileError(ValueError):
    pass


def _ns_from_ms(value: float) -> int:
    return int(float(value) * 1_000_000)


def compile_strategy_plan(
    spec: Mapping[str, Any],
    registry: PluginRegistry,
) -> CompiledStrategyPlan:
    strategy = spec.get("strategy", {})
    strategy_id = str(strategy.get("id", ""))
    strategy_version = str(strategy.get("version", ""))
    if not strategy_id or not strategy_version:
        raise PlanCompileError("strategy.id and strategy.version are required")

    provider_plugins = []
    for item in spec.get("context", {}).get("providers", []):
        provider_plugins.append(
            registry.resolve("feature_provider", str(item["id"]), str(item["version"]))
        )
    graph = compile_feature_graph(provider_plugins)

    schemas: dict[str, FeatureVectorSchema] = {}
    for schema_id, item in spec.get("context", {}).get("feature_vectors", {}).items():
        names = tuple(map(str, item.get("names", ())))
        defaults = tuple(float(x) for x in item.get("defaults", [0.0] * len(names)))
        schemas[str(schema_id)] = FeatureVectorSchema(names, defaults, str(item.get("version", "1")))

    templates: list[CandidateTemplate] = []
    for index, item in enumerate(spec.get("decision", {}).get("candidate_templates", [])):
        templates.append(
            CandidateTemplate(
                template_id=str(item.get("id", f"template_{index}")),
                entry_policy_id=str(item["entry"]),
                stop_policy_id=str(item["stop"]),
                exit_policy_id=str(item["exit"]),
                parameters=dict(item.get("parameters", {})),
                priority=int(item.get("priority", index)),
            )
        )
    templates.sort(key=lambda t: (t.priority, t.template_id))
    max_candidates = int(spec.get("decision", {}).get("max_candidates_per_event", len(templates) or 1))
    if len(templates) > max_candidates:
        templates = templates[:max_candidates]

    routes = tuple(
        ModelRoute(
            model_id=str(item["model_id"]),
            model_version=str(item.get("model_version", "1.0.0")),
            feature_schema_id=str(item["feature_schema_id"]),
            output_mapping=dict(item.get("output_mapping", {})),
            required=bool(item.get("required", True)),
        )
        for item in spec.get("decision", {}).get("model_routes", [])
    )
    abstain_raw = spec.get("decision", {}).get("abstention", {})
    abstention = AbstentionPolicy(
        minimum_probability=float(abstain_raw.get("minimum_probability", 0.5)),
        minimum_expected_r=float(abstain_raw.get("minimum_expected_r", 0.0)),
        maximum_uncertainty=(
            None if abstain_raw.get("maximum_uncertainty") is None
            else float(abstain_raw["maximum_uncertainty"])
        ),
        minimum_score_margin=float(abstain_raw.get("minimum_score_margin", 0.0)),
        required_context_keys=tuple(map(str, abstain_raw.get("required_context_keys", ()))),
    )
    weights_raw = spec.get("decision", {}).get("utility_weights", {})
    weights = UtilityWeights(**{k: float(v) for k, v in weights_raw.items()})
    latency_raw = spec.get("runtime", {}).get("latency_budget_ms", {})
    stage_limits = {
        str(k): _ns_from_ms(v)
        for k, v in latency_raw.items()
        if k not in {"total", "action_on_breach"}
    }
    total_limit = latency_raw.get("total")
    budget = LatencyBudget(
        stage_limits_ns=stage_limits,
        total_limit_ns=None if total_limit is None else _ns_from_ms(total_limit),
        action_on_breach=str(latency_raw.get("action_on_breach", "record")),
    )
    frozen = registry.freeze()
    plan_hash = stable_hash(spec, prefix="plan_")
    return CompiledStrategyPlan(
        strategy_id=strategy_id,
        strategy_version=strategy_version,
        plan_hash=plan_hash,
        feature_graph=graph,
        feature_schemas=schemas,
        candidate_templates=tuple(templates),
        plugin_registry=frozen,
        model_routes=routes,
        abstention_policy=abstention,
        utility_weights=weights,
        latency_budget=budget,
        max_candidates_per_event=max_candidates,
        fallback_mode=str(spec.get("runtime", {}).get("fallback_mode", "abstain")),
        metadata=dict(spec.get("metadata", {})),
    )
