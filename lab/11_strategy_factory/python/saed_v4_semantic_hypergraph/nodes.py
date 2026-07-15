from __future__ import annotations

from typing import Any

from .canonical import content_hash, stable_id
from .enums import EvidenceRole, NodeKind
from .models import TemporalNode


def build_node(
    *,
    kind: NodeKind,
    semantic_key: str,
    event_time: str,
    known_time: str,
    evidence_role: EvidenceRole,
    quality: float,
    missing: bool,
    masked: bool,
    source_hashes: tuple[str, ...] = (),
    attributes: dict[str, Any] | None = None,
) -> TemporalNode:
    attributes = attributes or {}
    seed = {
        "kind": kind.value,
        "semantic_key": semantic_key,
        "event_time": event_time,
        "known_time": known_time,
        "evidence_role": evidence_role.value,
        "source_hashes": sorted(source_hashes),
        "attributes": {key: attributes[key] for key in sorted(attributes)},
    }
    node_id = stable_id("hnode", seed)
    draft = TemporalNode(
        node_id=node_id,
        kind=kind,
        semantic_key=semantic_key,
        event_time=event_time,
        known_time=known_time,
        evidence_role=evidence_role,
        quality=round(float(quality), 12),
        missing=bool(missing),
        masked=bool(masked),
        source_hashes=tuple(sorted(set(source_hashes))),
        attributes=tuple(sorted(attributes.items())),
        node_hash="",
    )
    return TemporalNode(**{**draft.__dict__, "node_hash": content_hash(draft.semantic_payload())})
