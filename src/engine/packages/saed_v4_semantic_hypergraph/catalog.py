from __future__ import annotations

from .enums import NodeKind, RelationKind
from .models import (
    GraphBuildPolicy,
    HypergraphAuthorityBoundary,
    NodeTypeDefinition,
    RelationDefinition,
    Selector,
    SemanticRegistry,
    SemanticRelationRule,
)


def institutional_registry() -> SemanticRegistry:
    node_types = tuple(
        NodeTypeDefinition(kind=kind, description=f"Closed V4-05 {kind.value} node type.")
        for kind in NodeKind
    )
    relations = (
        RelationDefinition(
            RelationKind.CONTEXT_COMPOSITION,
            (NodeKind.CONTEXT, NodeKind.VIEW),
            2,
            32,
            True,
            description="Context and its exact-version view members.",
        ),
        RelationDefinition(
            RelationKind.VIEW_COMPOSITION,
            (NodeKind.VIEW, NodeKind.FEATURE),
            2,
            256,
            True,
            description="View and its deterministic feature members.",
        ),
        RelationDefinition(
            RelationKind.SOURCE_PROVENANCE,
            (NodeKind.FEATURE, NodeKind.SOURCE_ARTIFACT),
            2,
            64,
            False,
            description="Feature and the source artifacts that support it.",
        ),
        RelationDefinition(
            RelationKind.TEMPORAL_COHORT,
            (NodeKind.TEMPORAL_ANCHOR, NodeKind.FEATURE),
            2,
            512,
            False,
            description="Features sharing an exact visible event-time anchor.",
        ),
        RelationDefinition(
            RelationKind.CROSS_VIEW_ALIGNMENT,
            (NodeKind.CONTEXT, NodeKind.VIEW),
            3,
            32,
            True,
            description="Package-level exact-boundary alignment across views.",
        ),
        RelationDefinition(
            RelationKind.SEMANTIC_FAMILY,
            (NodeKind.CONTEXT, NodeKind.FEATURE),
            2,
            64,
            False,
            description="Explicit allowlisted semantic family; never inferred as canonical truth.",
        ),
        RelationDefinition(
            RelationKind.CONTEXT_ANCESTRY,
            (NodeKind.CONTEXT, NodeKind.EXTERNAL_CONTEXT_REFERENCE, NodeKind.FEATURE),
            2,
            16,
            False,
            description="Read-only ancestry relation represented by approved View features.",
        ),
        RelationDefinition(
            RelationKind.TREATMENT_DESCRIPTOR_BINDING,
            (NodeKind.CONTEXT, NodeKind.TREATMENT_DESCRIPTOR, NodeKind.FEATURE),
            2,
            32,
            False,
            description="Read-only binding to an externally approved Treatment descriptor.",
        ),
    )
    rules = (
        SemanticRelationRule(
            "market_price_execution_state",
            "1.0.0",
            RelationKind.SEMANTIC_FAMILY,
            (
                Selector("price_view", "mid"),
                Selector("price_view", "spread"),
                Selector("execution_view", "spread_points"),
                Selector("execution_view", "estimated_slippage_points"),
                Selector("execution_view", "latency_ms"),
            ),
            True,
            4,
            True,
            "Explicit relation across visible price and execution-state features.",
        ),
        SemanticRelationRule(
            "context_time_session_state",
            "1.0.0",
            RelationKind.SEMANTIC_FAMILY,
            (
                Selector("time_view", "hour_utc"),
                Selector("time_view", "weekday_utc"),
                Selector("time_view", "seconds_since_context_start"),
                Selector("session_view", "session_id"),
                Selector("session_view", "session_open"),
                Selector("session_view", "minutes_from_open"),
            ),
            True,
            5,
            True,
            "Explicit relation across visible temporal and session features.",
        ),
        SemanticRelationRule(
            "structure_ancestry_state",
            "1.0.0",
            RelationKind.SEMANTIC_FAMILY,
            (
                Selector("structure_view", "lifecycle_state"),
                Selector("structure_view", "twin_state"),
                Selector("context_ancestry_view", "context_family"),
                Selector("context_ancestry_view", "generation_depth"),
            ),
            True,
            3,
            False,
            "Explicit relation across current structure and ancestry descriptors.",
        ),
        SemanticRelationRule(
            "intermarket_liquidity_state",
            "1.0.0",
            RelationKind.SEMANTIC_FAMILY,
            (
                Selector("intermarket_view", "cross_market_state"),
                Selector("intermarket_view", "related_symbol_score"),
                Selector("liquidity_view", "liquidity_state"),
                Selector("liquidity_view", "quote_rate"),
                Selector("liquidity_view", "trade_rate"),
            ),
            True,
            3,
            False,
            "Explicit relation across intermarket and liquidity descriptors.",
        ),
    )
    return SemanticRegistry(
        registry_name="institutional_semantic_temporal_hypergraph_registry",
        exact_version="1.0.0",
        node_types=node_types,
        relations=relations,
        rules=rules,
        authority=HypergraphAuthorityBoundary(),
        limitations=(
            "Relations are deterministic and allowlisted; no edge is learned.",
            "The registry creates derived representation only and cannot mutate canonical Context truth.",
            "Treatment descriptor relations are read-only and carry no selection authority.",
        ),
    )


def institutional_policy() -> GraphBuildPolicy:
    return GraphBuildPolicy(
        policy_name="institutional_semantic_temporal_hypergraph_policy",
        exact_version="1.0.0",
        required_view_names=("price_view", "structure_view", "time_view"),
        allow_degraded_views=True,
        minimum_feature_quality=0.50,
        include_missing_feature_nodes=True,
        include_source_artifact_nodes=True,
        include_temporal_cohorts=True,
        maximum_nodes=4096,
        maximum_edges=8192,
        maximum_edge_arity=512,
        prohibited_feature_tokens=(
            "future",
            "target",
            "label",
            "outcome",
            "realized_pnl",
            "forward_return",
        ),
        deterministic_partition_count=16,
    )
