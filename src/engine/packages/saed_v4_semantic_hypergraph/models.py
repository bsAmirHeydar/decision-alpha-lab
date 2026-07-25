from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .canonical import content_hash, stable_id
from .enums import (
    EvidenceRole,
    GraphStatus,
    NodeKind,
    ProjectionKind,
    QueryDirection,
    RelationKind,
    SupportStatus,
)


@dataclass(frozen=True)
class HypergraphAuthorityBoundary:
    read_multimodal_package: bool = True
    read_view_lineage: bool = True
    build_hypergraph: bool = True
    replay_hypergraph: bool = True
    query_hypergraph: bool = True
    project_baseline: bool = True
    mutate_ucee_truth: bool = False
    mutate_view_artifacts: bool = False
    infer_canonical_relations: bool = False
    fit_adaptive_statistics: bool = False
    learn_edges: bool = False
    train_model: bool = False
    generate_treatment: bool = False
    select_treatment: bool = False
    allocate_risk: bool = False
    activate_runtime: bool = False
    send_order: bool = False
    network_access: bool = False

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class NodeTypeDefinition:
    kind: NodeKind
    required_attributes: tuple[str, ...] = ()
    prohibited_attributes: tuple[str, ...] = ()
    description: str = ""

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "required_attributes": sorted(self.required_attributes),
            "prohibited_attributes": sorted(self.prohibited_attributes),
            "description": self.description,
        }


@dataclass(frozen=True)
class RelationDefinition:
    kind: RelationKind
    allowed_node_kinds: tuple[NodeKind, ...]
    minimum_arity: int
    maximum_arity: int
    required: bool
    allow_repeated_kind: bool = True
    description: str = ""

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "allowed_node_kinds": sorted(kind.value for kind in self.allowed_node_kinds),
            "minimum_arity": self.minimum_arity,
            "maximum_arity": self.maximum_arity,
            "required": self.required,
            "allow_repeated_kind": self.allow_repeated_kind,
            "description": self.description,
        }


@dataclass(frozen=True)
class Selector:
    view_name: str
    feature_id: str

    @property
    def key(self) -> str:
        return f"{self.view_name}:{self.feature_id}"


@dataclass(frozen=True)
class SemanticRelationRule:
    rule_name: str
    exact_version: str
    relation_kind: RelationKind
    selectors: tuple[Selector, ...]
    include_context: bool
    minimum_members: int
    required: bool
    description: str = ""

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "rule_name": self.rule_name,
            "exact_version": self.exact_version,
            "relation_kind": self.relation_kind.value,
            "selectors": [
                {"view_name": selector.view_name, "feature_id": selector.feature_id}
                for selector in sorted(self.selectors, key=lambda item: item.key)
            ],
            "include_context": self.include_context,
            "minimum_members": self.minimum_members,
            "required": self.required,
            "description": self.description,
        }

    @property
    def rule_id(self) -> str:
        return stable_id("semrule", self.semantic_payload())


@dataclass(frozen=True)
class SemanticRegistry:
    registry_name: str
    exact_version: str
    node_types: tuple[NodeTypeDefinition, ...]
    relations: tuple[RelationDefinition, ...]
    rules: tuple[SemanticRelationRule, ...]
    authority: HypergraphAuthorityBoundary
    limitations: tuple[str, ...] = ()

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "registry_name": self.registry_name,
            "exact_version": self.exact_version,
            "node_types": [
                item.semantic_payload() for item in sorted(self.node_types, key=lambda item: item.kind.value)
            ],
            "relations": [
                item.semantic_payload() for item in sorted(self.relations, key=lambda item: item.kind.value)
            ],
            "rules": [item.semantic_payload() for item in sorted(self.rules, key=lambda item: item.rule_name)],
            "authority": self.authority.to_dict(),
            "limitations": sorted(self.limitations),
        }

    @property
    def registry_id(self) -> str:
        return stable_id("semreg", self.semantic_payload())

    @property
    def registry_hash(self) -> str:
        return content_hash(self.semantic_payload())


@dataclass(frozen=True)
class GraphBuildPolicy:
    policy_name: str
    exact_version: str
    required_view_names: tuple[str, ...]
    allow_degraded_views: bool
    minimum_feature_quality: float
    include_missing_feature_nodes: bool
    include_source_artifact_nodes: bool
    include_temporal_cohorts: bool
    maximum_nodes: int
    maximum_edges: int
    maximum_edge_arity: int
    prohibited_feature_tokens: tuple[str, ...]
    deterministic_partition_count: int = 1

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "policy_name": self.policy_name,
            "exact_version": self.exact_version,
            "required_view_names": sorted(self.required_view_names),
            "allow_degraded_views": self.allow_degraded_views,
            "minimum_feature_quality": self.minimum_feature_quality,
            "include_missing_feature_nodes": self.include_missing_feature_nodes,
            "include_source_artifact_nodes": self.include_source_artifact_nodes,
            "include_temporal_cohorts": self.include_temporal_cohorts,
            "maximum_nodes": self.maximum_nodes,
            "maximum_edges": self.maximum_edges,
            "maximum_edge_arity": self.maximum_edge_arity,
            "prohibited_feature_tokens": sorted(self.prohibited_feature_tokens),
            "deterministic_partition_count": self.deterministic_partition_count,
        }

    @property
    def policy_id(self) -> str:
        return stable_id("graphpolicy", self.semantic_payload())

    @property
    def policy_hash(self) -> str:
        return content_hash(self.semantic_payload())


@dataclass(frozen=True)
class TemporalNode:
    node_id: str
    kind: NodeKind
    semantic_key: str
    event_time: str
    known_time: str
    evidence_role: EvidenceRole
    quality: float
    missing: bool
    masked: bool
    source_hashes: tuple[str, ...]
    attributes: tuple[tuple[str, Any], ...]
    node_hash: str

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind.value,
            "semantic_key": self.semantic_key,
            "event_time": self.event_time,
            "known_time": self.known_time,
            "evidence_role": self.evidence_role.value,
            "quality": self.quality,
            "missing": self.missing,
            "masked": self.masked,
            "source_hashes": sorted(self.source_hashes),
            "attributes": {key: value for key, value in sorted(self.attributes)},
        }


@dataclass(frozen=True)
class TemporalHyperedge:
    edge_id: str
    relation_kind: RelationKind
    member_node_ids: tuple[str, ...]
    event_time_start: str
    event_time_end: str
    known_time: str
    evidence_role: EvidenceRole
    active: bool
    mask: int
    quality: float
    source_rule_id: str | None
    reason_codes: tuple[str, ...]
    edge_hash: str

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "relation_kind": self.relation_kind.value,
            "member_node_ids": sorted(self.member_node_ids),
            "event_time_start": self.event_time_start,
            "event_time_end": self.event_time_end,
            "known_time": self.known_time,
            "evidence_role": self.evidence_role.value,
            "active": self.active,
            "mask": self.mask,
            "quality": self.quality,
            "source_rule_id": self.source_rule_id,
            "reason_codes": sorted(self.reason_codes),
        }


@dataclass(frozen=True)
class GraphSupportAssessment:
    status: SupportStatus
    node_count: int
    edge_count: int
    active_edge_count: int
    required_relation_total: int
    required_relation_present: int
    missing_required_relations: tuple[str, ...]
    missing_required_views: tuple[str, ...]
    degraded_node_ids: tuple[str, ...]
    reasons: tuple[str, ...]

    @property
    def assessment_id(self) -> str:
        payload = asdict(self)
        payload["status"] = self.status.value
        return stable_id("graphsupport", payload)


@dataclass(frozen=True)
class SemanticTemporalHypergraph:
    graph_id: str
    graph_version: str
    registry_id: str
    registry_hash: str
    policy_id: str
    policy_hash: str
    source_package_id: str
    source_package_hash: str
    twin_id: str
    known_as_of: str
    event_as_of: str
    evidence_role: EvidenceRole
    status: GraphStatus
    nodes: tuple[TemporalNode, ...]
    edges: tuple[TemporalHyperedge, ...]
    support: GraphSupportAssessment
    lineage_root: str
    graph_hash: str
    limitations: tuple[str, ...]

    def semantic_payload(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "graph_version": self.graph_version,
            "registry_id": self.registry_id,
            "registry_hash": self.registry_hash,
            "policy_id": self.policy_id,
            "policy_hash": self.policy_hash,
            "source_package_id": self.source_package_id,
            "source_package_hash": self.source_package_hash,
            "twin_id": self.twin_id,
            "known_as_of": self.known_as_of,
            "event_as_of": self.event_as_of,
            "evidence_role": self.evidence_role.value,
            "status": self.status.value,
            "node_hashes": sorted(node.node_hash for node in self.nodes),
            "edge_hashes": sorted(edge.edge_hash for edge in self.edges),
            "support": {
                **asdict(self.support),
                "status": self.support.status.value,
            },
            "lineage_root": self.lineage_root,
            "limitations": sorted(self.limitations),
        }


@dataclass(frozen=True)
class GraphIntegrityReceipt:
    graph_id: str
    graph_hash: str
    source_package_hash: str
    registry_hash: str
    policy_hash: str
    node_hashes: tuple[str, ...]
    edge_hashes: tuple[str, ...]
    component_root: str
    status: str

    @property
    def receipt_id(self) -> str:
        return stable_id("graphintegrity", asdict(self))


@dataclass(frozen=True)
class GraphReplayReceipt:
    graph_id: str
    expected_graph_hash: str
    observed_graph_hash: str
    source_package_hash: str
    registry_hash: str
    policy_hash: str
    status: str

    @property
    def receipt_id(self) -> str:
        return stable_id("graphreplay", asdict(self))


@dataclass(frozen=True)
class GraphDiff:
    left_graph_hash: str
    right_graph_hash: str
    added_node_ids: tuple[str, ...]
    removed_node_ids: tuple[str, ...]
    changed_node_ids: tuple[str, ...]
    added_edge_ids: tuple[str, ...]
    removed_edge_ids: tuple[str, ...]
    changed_edge_ids: tuple[str, ...]
    status_changed: bool
    support_changed: bool

    @property
    def diff_id(self) -> str:
        return stable_id("graphdiff", asdict(self))


@dataclass(frozen=True)
class GraphProjection:
    projection_id: str
    graph_id: str
    graph_hash: str
    kind: ProjectionKind
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...]
    rows: tuple[tuple[int, ...], ...]
    projection_hash: str
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class GraphQuery:
    query_id: str
    seed_node_ids: tuple[str, ...]
    relation_kinds: tuple[RelationKind, ...]
    node_kinds: tuple[NodeKind, ...]
    direction: QueryDirection
    maximum_hops: int
    maximum_results: int
    include_masked: bool = False


@dataclass(frozen=True)
class GraphQueryResult:
    query_id: str
    graph_id: str
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...]
    truncated: bool
    result_hash: str


@dataclass(frozen=True)
class PartitionManifest:
    graph_id: str
    graph_hash: str
    partition_count: int
    node_partitions: tuple[tuple[str, int], ...]
    edge_partitions: tuple[tuple[str, int], ...]
    manifest_hash: str


@dataclass(frozen=True)
class HypergraphTelemetry:
    operation: str
    graph_id: str | None
    source_package_id: str
    node_count: int
    edge_count: int
    masked_edge_count: int
    degraded_node_count: int
    deterministic: bool
    authority_violation_count: int
    telemetry_hash: str = field(default="")
