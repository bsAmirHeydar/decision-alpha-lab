from __future__ import annotations

from .canonical import content_hash, stable_id
from .enums import EvidenceRole, RelationKind
from .models import TemporalHyperedge, TemporalNode


def build_edge(
    *,
    relation_kind: RelationKind,
    members: tuple[TemporalNode, ...],
    evidence_role: EvidenceRole,
    source_rule_id: str | None = None,
    reason_codes: tuple[str, ...] = (),
) -> TemporalHyperedge:
    unique = {node.node_id: node for node in members}
    ordered = tuple(unique[node_id] for node_id in sorted(unique))
    active = bool(ordered) and all(not node.masked for node in ordered)
    quality = min((node.quality for node in ordered), default=0.0)
    event_times = sorted(node.event_time for node in ordered)
    known_times = sorted(node.known_time for node in ordered)
    seed = {
        "relation_kind": relation_kind.value,
        "member_node_ids": [node.node_id for node in ordered],
        "event_time_start": event_times[0],
        "event_time_end": event_times[-1],
        "known_time": known_times[-1],
        "evidence_role": evidence_role.value,
        "source_rule_id": source_rule_id,
    }
    edge_id = stable_id("hedge", seed)
    draft = TemporalHyperedge(
        edge_id=edge_id,
        relation_kind=relation_kind,
        member_node_ids=tuple(node.node_id for node in ordered),
        event_time_start=event_times[0],
        event_time_end=event_times[-1],
        known_time=known_times[-1],
        evidence_role=evidence_role,
        active=active,
        mask=0 if active else 1,
        quality=round(float(quality), 12),
        source_rule_id=source_rule_id,
        reason_codes=tuple(sorted(set(reason_codes + (() if active else ("masked_member",))))),
        edge_hash="",
    )
    return TemporalHyperedge(**{**draft.__dict__, "edge_hash": content_hash(draft.semantic_payload())})
