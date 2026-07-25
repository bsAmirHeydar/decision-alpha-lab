from __future__ import annotations

from typing import Any

from .builder import SemanticTemporalHypergraphBuilder
from .errors import IntegrityError
from .models import GraphBuildPolicy, GraphReplayReceipt, SemanticRegistry, SemanticTemporalHypergraph


def replay_graph(
    *,
    expected: SemanticTemporalHypergraph,
    package: Any,
    registry: SemanticRegistry,
    policy: GraphBuildPolicy,
) -> GraphReplayReceipt:
    observed = SemanticTemporalHypergraphBuilder().build(
        package=package,
        registry=registry,
        policy=policy,
        graph_version=expected.graph_version,
    )
    status = "pass" if observed.graph_hash == expected.graph_hash else "fail"
    receipt = GraphReplayReceipt(
        graph_id=expected.graph_id,
        expected_graph_hash=expected.graph_hash,
        observed_graph_hash=observed.graph_hash,
        source_package_hash=package.package_hash,
        registry_hash=registry.registry_hash,
        policy_hash=policy.policy_hash,
        status=status,
    )
    if status != "pass":
        raise IntegrityError("deterministic graph replay mismatch")
    return receipt
