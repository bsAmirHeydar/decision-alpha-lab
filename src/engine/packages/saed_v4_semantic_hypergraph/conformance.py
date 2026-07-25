from __future__ import annotations

from dataclasses import replace
from typing import Any

from .builder import SemanticTemporalHypergraphBuilder
from .catalog import institutional_policy, institutional_registry
from .errors import HypergraphError


def run_conformance(package: Any) -> dict:
    registry = institutional_registry()
    policy = institutional_policy()
    builder = SemanticTemporalHypergraphBuilder()
    graph = builder.build(package, registry, policy)
    checks = {
        "deterministic_rebuild": builder.build(package, registry, policy).graph_hash == graph.graph_hash,
        "order_invariant_registry_rules": builder.build(
            package,
            replace(registry, rules=tuple(reversed(registry.rules))),
            policy,
        ).graph_hash == graph.graph_hash,
        "no_training_authority": not registry.authority.train_model,
        "no_treatment_selection_authority": not registry.authority.select_treatment,
        "no_execution_authority": not registry.authority.send_order,
        "closed_relation_catalog": len(registry.relations) == len(set(item.kind for item in registry.relations)),
        "hash_bound_source": graph.source_package_hash == package.package_hash,
    }
    return {
        "phase": "SAED_V4_05",
        "graph_id": graph.graph_id,
        "graph_hash": graph.graph_hash,
        "checks": checks,
        "status": "pass" if all(checks.values()) else "fail",
    }
