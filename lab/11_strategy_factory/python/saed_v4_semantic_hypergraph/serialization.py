from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .models import SemanticTemporalHypergraph, TemporalHyperedge, TemporalNode


def to_document(value: Any) -> Any:
    """Serialize contract objects into their public closed-schema representation."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, TemporalNode):
        return {**value.semantic_payload(), "node_hash": value.node_hash}
    if isinstance(value, TemporalHyperedge):
        return {**value.semantic_payload(), "edge_hash": value.edge_hash}
    if isinstance(value, SemanticTemporalHypergraph):
        return {
            "graph_id": value.graph_id,
            "graph_version": value.graph_version,
            "registry_id": value.registry_id,
            "registry_hash": value.registry_hash,
            "policy_id": value.policy_id,
            "policy_hash": value.policy_hash,
            "source_package_id": value.source_package_id,
            "source_package_hash": value.source_package_hash,
            "twin_id": value.twin_id,
            "known_as_of": value.known_as_of,
            "event_as_of": value.event_as_of,
            "evidence_role": value.evidence_role.value,
            "status": value.status.value,
            "nodes": [to_document(node) for node in value.nodes],
            "edges": [to_document(edge) for edge in value.edges],
            "support": to_document(value.support),
            "lineage_root": value.lineage_root,
            "graph_hash": value.graph_hash,
            "limitations": sorted(value.limitations),
        }
    if is_dataclass(value):
        return {field.name: to_document(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, dict):
        return {str(key): to_document(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_document(item) for item in value]
    if isinstance(value, set):
        return sorted(to_document(item) for item in value)
    return value


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(to_document(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
