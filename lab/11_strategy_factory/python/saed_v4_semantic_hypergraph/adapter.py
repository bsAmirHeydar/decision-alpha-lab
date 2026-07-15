from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import content_hash
from .enums import EvidenceRole, NodeKind
from .errors import GraphBuildError
from .models import GraphBuildPolicy, TemporalNode
from .nodes import build_node


@dataclass(frozen=True)
class AdaptedPackage:
    context_node: TemporalNode
    view_nodes: tuple[TemporalNode, ...]
    feature_nodes: tuple[TemporalNode, ...]
    source_nodes: tuple[TemporalNode, ...]
    temporal_nodes: tuple[TemporalNode, ...]
    external_context_nodes: tuple[TemporalNode, ...]
    treatment_nodes: tuple[TemporalNode, ...]
    feature_index: dict[str, TemporalNode]
    view_index: dict[str, TemporalNode]
    feature_to_sources: dict[str, tuple[TemporalNode, ...]]
    feature_to_view: dict[str, TemporalNode]


def adapt_multimodal_package(package: Any, policy: GraphBuildPolicy) -> AdaptedPackage:
    role = EvidenceRole(package.evidence_role.value if hasattr(package.evidence_role, "value") else package.evidence_role)
    context_node = build_node(
        kind=NodeKind.CONTEXT,
        semantic_key=f"context:{package.twin_id}",
        event_time=package.event_as_of,
        known_time=package.known_as_of,
        evidence_role=role,
        quality=min(package.quality_vector) if package.quality_vector else 0.0,
        missing=False,
        masked=False,
        source_hashes=(package.package_hash,),
        attributes={
            "twin_id": package.twin_id,
            "source_package_id": package.package_id,
            "source_package_hash": package.package_hash,
        },
    )
    view_nodes: list[TemporalNode] = []
    feature_nodes: list[TemporalNode] = []
    source_nodes_by_key: dict[str, TemporalNode] = {}
    temporal_nodes_by_time: dict[str, TemporalNode] = {}
    external_context_nodes_by_key: dict[str, TemporalNode] = {}
    treatment_nodes_by_key: dict[str, TemporalNode] = {}
    feature_index: dict[str, TemporalNode] = {}
    view_index: dict[str, TemporalNode] = {}
    feature_to_sources: dict[str, tuple[TemporalNode, ...]] = {}
    feature_to_view: dict[str, TemporalNode] = {}

    for view in sorted(package.views, key=lambda item: (item.view_name, item.exact_version, item.view_hash)):
        view_quality = min((feature.quality for feature in view.features), default=0.0)
        view_masked = view.status.value not in {"complete", "degraded"}
        view_node = build_node(
            kind=NodeKind.VIEW,
            semantic_key=f"view:{view.view_name}:{view.exact_version}",
            event_time=view.event_as_of,
            known_time=view.known_as_of,
            evidence_role=role,
            quality=view_quality,
            missing=False,
            masked=view_masked,
            source_hashes=(view.view_hash, view.specification_hash),
            attributes={
                "view_name": view.view_name,
                "exact_version": view.exact_version,
                "view_id": view.view_id,
                "view_hash": view.view_hash,
                "view_status": view.status.value,
                "support_status": view.support.status.value,
            },
        )
        view_nodes.append(view_node)
        view_index[view.view_name] = view_node
        for feature in sorted(view.features, key=lambda item: item.feature_id):
            semantic_key = f"feature:{view.view_name}:{feature.feature_id}"
            lowered = semantic_key.lower()
            if any(token.lower() in lowered for token in policy.prohibited_feature_tokens):
                raise GraphBuildError(f"prohibited feature token in {semantic_key}")
            if feature.missing and not policy.include_missing_feature_nodes:
                continue
            event_time = feature.last_event_time or view.event_as_of
            masked = bool(feature.missing or feature.stale or feature.quality < policy.minimum_feature_quality)
            feature_node = build_node(
                kind=NodeKind.FEATURE,
                semantic_key=semantic_key,
                event_time=event_time,
                known_time=view.known_as_of,
                evidence_role=role,
                quality=feature.quality,
                missing=feature.missing,
                masked=masked,
                source_hashes=feature.source_value_hashes,
                attributes={
                    "view_name": view.view_name,
                    "feature_id": feature.feature_id,
                    "value": feature.value,
                    "normalized_value": feature.normalized_value,
                    "stale": feature.stale,
                    "mask": feature.mask,
                    "reason_codes": list(feature.reason_codes),
                },
            )
            feature_nodes.append(feature_node)
            feature_index[f"{view.view_name}:{feature.feature_id}"] = feature_node
            feature_to_view[feature_node.node_id] = view_node
            if policy.include_source_artifact_nodes:
                if len(feature.source_artifact_ids) != len(feature.source_value_hashes):
                    raise GraphBuildError(
                        f"source artifact/hash cardinality mismatch for {semantic_key}"
                    )
                supporting_nodes: list[TemporalNode] = []
                for artifact_id, value_hash in zip(feature.source_artifact_ids, feature.source_value_hashes):
                    key = f"{artifact_id}:{value_hash}"
                    if key not in source_nodes_by_key:
                        source_nodes_by_key[key] = build_node(
                            kind=NodeKind.SOURCE_ARTIFACT,
                            semantic_key=f"source_artifact:{artifact_id}",
                            event_time=event_time,
                            known_time=view.known_as_of,
                            evidence_role=role,
                            quality=feature.quality,
                            missing=False,
                            masked=masked,
                            source_hashes=(value_hash,),
                            attributes={"artifact_id": artifact_id, "value_hash": value_hash},
                        )
                    supporting_nodes.append(source_nodes_by_key[key])
                feature_to_sources[feature_node.node_id] = tuple(sorted(supporting_nodes, key=lambda item: item.node_id))
            if policy.include_temporal_cohorts:
                if event_time not in temporal_nodes_by_time:
                    temporal_nodes_by_time[event_time] = build_node(
                        kind=NodeKind.TEMPORAL_ANCHOR,
                        semantic_key=f"temporal_anchor:{event_time}",
                        event_time=event_time,
                        known_time=view.known_as_of,
                        evidence_role=role,
                        quality=1.0,
                        missing=False,
                        masked=False,
                        source_hashes=(content_hash(event_time),),
                        attributes={"anchor_time": event_time},
                    )
            if view.view_name == "context_ancestry_view" and feature.feature_id == "parent_context_id" and not feature.missing and feature.value:
                key = str(feature.value)
                external_context_nodes_by_key.setdefault(
                    key,
                    build_node(
                        kind=NodeKind.EXTERNAL_CONTEXT_REFERENCE,
                        semantic_key=f"external_context:{key}",
                        event_time=event_time,
                        known_time=view.known_as_of,
                        evidence_role=role,
                        quality=feature.quality,
                        missing=False,
                        masked=masked,
                        source_hashes=feature.source_value_hashes,
                        attributes={"external_context_id": key, "reference_only": True},
                    ),
                )
            if view.view_name == "treatment_descriptor_view" and feature.feature_id == "descriptor_id" and not feature.missing and feature.value:
                key = str(feature.value)
                treatment_nodes_by_key.setdefault(
                    key,
                    build_node(
                        kind=NodeKind.TREATMENT_DESCRIPTOR,
                        semantic_key=f"treatment_descriptor:{key}",
                        event_time=event_time,
                        known_time=view.known_as_of,
                        evidence_role=role,
                        quality=feature.quality,
                        missing=False,
                        masked=masked,
                        source_hashes=feature.source_value_hashes,
                        attributes={"descriptor_id": key, "read_only": True},
                    ),
                )

    return AdaptedPackage(
        context_node=context_node,
        view_nodes=tuple(sorted(view_nodes, key=lambda item: item.node_id)),
        feature_nodes=tuple(sorted(feature_nodes, key=lambda item: item.node_id)),
        source_nodes=tuple(sorted(source_nodes_by_key.values(), key=lambda item: item.node_id)),
        temporal_nodes=tuple(sorted(temporal_nodes_by_time.values(), key=lambda item: item.node_id)),
        external_context_nodes=tuple(sorted(external_context_nodes_by_key.values(), key=lambda item: item.node_id)),
        treatment_nodes=tuple(sorted(treatment_nodes_by_key.values(), key=lambda item: item.node_id)),
        feature_index=feature_index,
        view_index=view_index,
        feature_to_sources=feature_to_sources,
        feature_to_view=feature_to_view,
    )
