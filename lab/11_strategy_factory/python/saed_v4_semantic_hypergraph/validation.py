from __future__ import annotations

from collections import Counter
from typing import Any

from .canonical import content_hash, merkle_root
from .enums import GraphStatus
from .errors import GraphValidationError
from .models import GraphBuildPolicy, SemanticRegistry, SemanticTemporalHypergraph
from .temporal import validate_boundary, validate_interval


def validate_source_package(package: Any, policy: GraphBuildPolicy) -> None:
    if not package.package_id or not package.package_hash:
        raise GraphValidationError("source package identity is required")
    observed_hash = content_hash(package.semantic_payload())
    if observed_hash != package.package_hash:
        raise GraphValidationError("source multimodal package hash mismatch")
    compatibility = package.compatibility.status.value
    if compatibility == "incompatible":
        raise GraphValidationError("incompatible multimodal package")
    if compatibility == "degraded" and not policy.allow_degraded_views:
        raise GraphValidationError("degraded multimodal package is prohibited by policy")
    names = {view.view_name for view in package.views}
    missing = sorted(set(policy.required_view_names) - names)
    if missing:
        raise GraphValidationError(f"required views absent: {missing}")


def validate_graph(
    graph: SemanticTemporalHypergraph,
    registry: SemanticRegistry,
    policy: GraphBuildPolicy,
) -> None:
    if graph.registry_hash != registry.registry_hash or graph.registry_id != registry.registry_id:
        raise GraphValidationError("registry identity mismatch")
    if graph.policy_hash != policy.policy_hash or graph.policy_id != policy.policy_id:
        raise GraphValidationError("policy identity mismatch")
    if len(graph.nodes) > policy.maximum_nodes:
        raise GraphValidationError("node budget exceeded")
    if len(graph.edges) > policy.maximum_edges:
        raise GraphValidationError("edge budget exceeded")
    node_ids = [node.node_id for node in graph.nodes]
    edge_ids = [edge.edge_id for edge in graph.edges]
    if len(node_ids) != len(set(node_ids)):
        raise GraphValidationError("duplicate node identity")
    if len(edge_ids) != len(set(edge_ids)):
        raise GraphValidationError("duplicate edge identity")
    allowed_relations = {definition.kind: definition for definition in registry.relations}
    nodes_by_id = {node.node_id: node for node in graph.nodes}
    for node in graph.nodes:
        validate_boundary(node.event_time, node.known_time, graph.event_as_of, graph.known_as_of)
        if node.evidence_role != graph.evidence_role:
            raise GraphValidationError("cross-role node detected")
        if content_hash(node.semantic_payload()) != node.node_hash:
            raise GraphValidationError(f"node hash mismatch: {node.node_id}")
    for edge in graph.edges:
        validate_interval(
            edge.event_time_start,
            edge.event_time_end,
            edge.known_time,
            graph.event_as_of,
            graph.known_as_of,
        )
        if edge.evidence_role != graph.evidence_role:
            raise GraphValidationError("cross-role edge detected")
        if edge.relation_kind not in allowed_relations:
            raise GraphValidationError(f"unknown relation kind: {edge.relation_kind.value}")
        if len(edge.member_node_ids) != len(set(edge.member_node_ids)):
            raise GraphValidationError("duplicate incidence within edge")
        if any(node_id not in nodes_by_id for node_id in edge.member_node_ids):
            raise GraphValidationError("dangling edge incidence")
        definition = allowed_relations[edge.relation_kind]
        arity = len(edge.member_node_ids)
        if arity < definition.minimum_arity or arity > min(definition.maximum_arity, policy.maximum_edge_arity):
            raise GraphValidationError(f"invalid arity for {edge.relation_kind.value}: {arity}")
        kinds = [nodes_by_id[node_id].kind for node_id in edge.member_node_ids]
        if any(kind not in definition.allowed_node_kinds for kind in kinds):
            raise GraphValidationError(f"invalid node kind in relation {edge.relation_kind.value}")
        if not definition.allow_repeated_kind and any(count > 1 for count in Counter(kinds).values()):
            raise GraphValidationError(f"repeated node kind prohibited for {edge.relation_kind.value}")
        if content_hash(edge.semantic_payload()) != edge.edge_hash:
            raise GraphValidationError(f"edge hash mismatch: {edge.edge_id}")
    expected_lineage = merkle_root(
        [
            graph.source_package_hash,
            graph.registry_hash,
            graph.policy_hash,
            *(node.node_hash for node in graph.nodes),
            *(edge.edge_hash for edge in graph.edges),
        ]
    )
    if graph.lineage_root != expected_lineage:
        raise GraphValidationError("graph lineage root mismatch")
    if content_hash(graph.semantic_payload()) != graph.graph_hash:
        raise GraphValidationError("graph hash mismatch")
    expected_status = {
        "supported": GraphStatus.COMPLETE,
        "degraded": GraphStatus.DEGRADED,
        "unsupported": GraphStatus.UNSUPPORTED,
    }[graph.support.status.value]
    if graph.status != expected_status:
        raise GraphValidationError("graph status is inconsistent with support assessment")
