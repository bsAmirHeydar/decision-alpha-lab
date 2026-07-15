from __future__ import annotations

from collections import defaultdict
from typing import Any

from .adapter import AdaptedPackage, adapt_multimodal_package
from .canonical import content_hash, merkle_root, stable_id
from .edges import build_edge
from .enums import GraphStatus, RelationKind, SupportStatus
from .errors import GraphBuildError
from .models import (
    GraphBuildPolicy,
    SemanticRegistry,
    SemanticTemporalHypergraph,
    TemporalHyperedge,
    TemporalNode,
)
from .registry import validate_policy, validate_registry
from .support import assess_support
from .validation import validate_graph, validate_source_package


class SemanticTemporalHypergraphBuilder:
    """Deterministic V4-05 builder over an immutable V4-04 multimodal package."""

    def build(
        self,
        package: Any,
        registry: SemanticRegistry,
        policy: GraphBuildPolicy,
        graph_version: str = "1.0.0",
    ) -> SemanticTemporalHypergraph:
        validate_registry(registry)
        validate_policy(policy)
        validate_source_package(package, policy)
        adapted = adapt_multimodal_package(package, policy)
        nodes = self._nodes(adapted)
        edges = self._edges(package, adapted, registry)
        if len(nodes) > policy.maximum_nodes:
            raise GraphBuildError(f"node budget exceeded: {len(nodes)} > {policy.maximum_nodes}")
        if len(edges) > policy.maximum_edges:
            raise GraphBuildError(f"edge budget exceeded: {len(edges)} > {policy.maximum_edges}")
        if any(len(edge.member_node_ids) > policy.maximum_edge_arity for edge in edges):
            raise GraphBuildError("edge arity budget exceeded")
        support = assess_support(
            nodes=nodes,
            edges=edges,
            registry=registry,
            required_view_names=policy.required_view_names,
        )
        if support.status == SupportStatus.SUPPORTED:
            status = GraphStatus.COMPLETE
        elif support.status == SupportStatus.DEGRADED:
            status = GraphStatus.DEGRADED
        else:
            status = GraphStatus.UNSUPPORTED
        lineage_root = merkle_root(
            [
                package.package_hash,
                registry.registry_hash,
                policy.policy_hash,
                *(node.node_hash for node in nodes),
                *(edge.edge_hash for edge in edges),
            ]
        )
        seed = {
            "graph_version": graph_version,
            "registry_hash": registry.registry_hash,
            "policy_hash": policy.policy_hash,
            "source_package_hash": package.package_hash,
            "known_as_of": package.known_as_of,
            "event_as_of": package.event_as_of,
            "evidence_role": package.evidence_role.value,
            "node_hashes": sorted(node.node_hash for node in nodes),
            "edge_hashes": sorted(edge.edge_hash for edge in edges),
        }
        graph_id = stable_id("sthypergraph", seed)
        draft = SemanticTemporalHypergraph(
            graph_id=graph_id,
            graph_version=graph_version,
            registry_id=registry.registry_id,
            registry_hash=registry.registry_hash,
            policy_id=policy.policy_id,
            policy_hash=policy.policy_hash,
            source_package_id=package.package_id,
            source_package_hash=package.package_hash,
            twin_id=package.twin_id,
            known_as_of=package.known_as_of,
            event_as_of=package.event_as_of,
            evidence_role=adapted.context_node.evidence_role,
            status=status,
            nodes=nodes,
            edges=edges,
            support=support,
            lineage_root=lineage_root,
            graph_hash="",
            limitations=tuple(
                sorted(
                    set(registry.limitations)
                    | {
                        "V4-05 constructs deterministic representation only; it does not train a graph model.",
                        "Unknown relations remain absent or masked and are never inferred into canonical truth.",
                        "The graph cannot generate or select Treatments, allocate risk, activate runtime, or send orders.",
                    }
                )
            ),
        )
        graph = SemanticTemporalHypergraph(
            **{**draft.__dict__, "graph_hash": content_hash(draft.semantic_payload())}
        )
        validate_graph(graph, registry, policy)
        return graph

    @staticmethod
    def _nodes(adapted: AdaptedPackage) -> tuple[TemporalNode, ...]:
        nodes = (
            (adapted.context_node,)
            + adapted.view_nodes
            + adapted.feature_nodes
            + adapted.source_nodes
            + adapted.temporal_nodes
            + adapted.external_context_nodes
            + adapted.treatment_nodes
        )
        return tuple(sorted(nodes, key=lambda item: (item.kind.value, item.semantic_key, item.node_id)))

    def _edges(
        self,
        package: Any,
        adapted: AdaptedPackage,
        registry: SemanticRegistry,
    ) -> tuple[TemporalHyperedge, ...]:
        role = adapted.context_node.evidence_role
        edges: list[TemporalHyperedge] = []
        edges.append(
            build_edge(
                relation_kind=RelationKind.CONTEXT_COMPOSITION,
                members=(adapted.context_node,) + adapted.view_nodes,
                evidence_role=role,
            )
        )
        edges.append(
            build_edge(
                relation_kind=RelationKind.CROSS_VIEW_ALIGNMENT,
                members=(adapted.context_node,) + adapted.view_nodes,
                evidence_role=role,
            )
        )
        features_by_view: dict[str, list[TemporalNode]] = defaultdict(list)
        for feature in adapted.feature_nodes:
            features_by_view[dict(feature.attributes)["view_name"]].append(feature)
        for view_name, feature_nodes in sorted(features_by_view.items()):
            view_node = adapted.view_index[view_name]
            edges.append(
                build_edge(
                    relation_kind=RelationKind.VIEW_COMPOSITION,
                    members=(view_node,) + tuple(feature_nodes),
                    evidence_role=role,
                )
            )
        for feature_node_id, source_nodes in sorted(adapted.feature_to_sources.items()):
            if source_nodes:
                feature = next(node for node in adapted.feature_nodes if node.node_id == feature_node_id)
                edges.append(
                    build_edge(
                        relation_kind=RelationKind.SOURCE_PROVENANCE,
                        members=(feature,) + source_nodes,
                        evidence_role=role,
                    )
                )
        features_by_time: dict[str, list[TemporalNode]] = defaultdict(list)
        for feature in adapted.feature_nodes:
            features_by_time[feature.event_time].append(feature)
        temporal_by_time = {dict(node.attributes)["anchor_time"]: node for node in adapted.temporal_nodes}
        for event_time, features in sorted(features_by_time.items()):
            if event_time in temporal_by_time:
                edges.append(
                    build_edge(
                        relation_kind=RelationKind.TEMPORAL_COHORT,
                        members=(temporal_by_time[event_time],) + tuple(features),
                        evidence_role=role,
                    )
                )
        for rule in sorted(registry.rules, key=lambda item: item.rule_name):
            selected = [adapted.feature_index[selector.key] for selector in rule.selectors if selector.key in adapted.feature_index]
            members = ((adapted.context_node,) if rule.include_context else ()) + tuple(selected)
            if len(members) < rule.minimum_members:
                continue
            edges.append(
                build_edge(
                    relation_kind=rule.relation_kind,
                    members=members,
                    evidence_role=role,
                    source_rule_id=rule.rule_id,
                )
            )
        parent_feature = adapted.feature_index.get("context_ancestry_view:parent_context_id")
        if parent_feature and adapted.external_context_nodes:
            edges.append(
                build_edge(
                    relation_kind=RelationKind.CONTEXT_ANCESTRY,
                    members=(adapted.context_node, parent_feature) + adapted.external_context_nodes,
                    evidence_role=role,
                )
            )
        descriptor_feature = adapted.feature_index.get("treatment_descriptor_view:descriptor_id")
        if descriptor_feature and adapted.treatment_nodes:
            treatment_features = tuple(
                node
                for key, node in adapted.feature_index.items()
                if key.startswith("treatment_descriptor_view:")
            )
            edges.append(
                build_edge(
                    relation_kind=RelationKind.TREATMENT_DESCRIPTOR_BINDING,
                    members=(adapted.context_node,) + adapted.treatment_nodes + treatment_features,
                    evidence_role=role,
                )
            )
        unique = {edge.edge_id: edge for edge in edges}
        return tuple(sorted(unique.values(), key=lambda item: (item.relation_kind.value, item.edge_id)))
