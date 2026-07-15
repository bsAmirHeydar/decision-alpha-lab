from __future__ import annotations

from .enums import SupportStatus
from .models import GraphSupportAssessment, SemanticRegistry, TemporalHyperedge, TemporalNode


def assess_support(
    *,
    nodes: tuple[TemporalNode, ...],
    edges: tuple[TemporalHyperedge, ...],
    registry: SemanticRegistry,
    required_view_names: tuple[str, ...],
) -> GraphSupportAssessment:
    active_kinds = {edge.relation_kind for edge in edges if edge.active}
    active_rule_ids = {edge.source_rule_id for edge in edges if edge.active and edge.source_rule_id}
    required_relations = {definition.kind for definition in registry.relations if definition.required}
    missing_relation_kinds = {kind.value for kind in required_relations - active_kinds}
    missing_rule_names = {
        f"semantic_rule:{rule.rule_name}"
        for rule in registry.rules
        if rule.required and rule.rule_id not in active_rule_ids
    }
    missing_relations = tuple(sorted(missing_relation_kinds | missing_rule_names))
    view_nodes = {
        dict(node.attributes).get("view_name"): node
        for node in nodes
        if node.kind.value == "view" and not node.masked
    }
    active_view_composition_members = {
        node_id
        for edge in edges
        if edge.active and edge.relation_kind.value == "view_composition"
        for node_id in edge.member_node_ids
    }
    present_views = {
        view_name
        for view_name, node in view_nodes.items()
        if view_name and node.node_id in active_view_composition_members
    }
    missing_views = tuple(sorted(set(required_view_names) - present_views))
    degraded_nodes = tuple(sorted(node.node_id for node in nodes if node.masked or node.quality < 1.0))
    reasons: list[str] = []
    if missing_relations:
        reasons.append("missing_required_relations")
    if missing_views:
        reasons.append("missing_required_views")
    if degraded_nodes:
        reasons.append("degraded_or_masked_nodes")
    if missing_relations or missing_views:
        status = SupportStatus.UNSUPPORTED
    elif degraded_nodes:
        status = SupportStatus.DEGRADED
    else:
        status = SupportStatus.SUPPORTED
    return GraphSupportAssessment(
        status=status,
        node_count=len(nodes),
        edge_count=len(edges),
        active_edge_count=sum(edge.active for edge in edges),
        required_relation_total=len(required_relations) + sum(rule.required for rule in registry.rules),
        required_relation_present=(
            len(required_relations & active_kinds)
            + sum(rule.required and rule.rule_id in active_rule_ids for rule in registry.rules)
        ),
        missing_required_relations=missing_relations,
        missing_required_views=missing_views,
        degraded_node_ids=degraded_nodes,
        reasons=tuple(sorted(reasons)),
    )
