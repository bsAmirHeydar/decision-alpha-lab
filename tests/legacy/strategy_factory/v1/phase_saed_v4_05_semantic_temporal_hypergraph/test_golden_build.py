from helpers import build_graph
from saed_v4_semantic_hypergraph.enums import GraphStatus, NodeKind, RelationKind


def test_golden_graph_is_complete():
    graph = build_graph()
    assert graph.status == GraphStatus.COMPLETE
    assert graph.support.status.value == "supported"
    assert graph.graph_hash
    assert graph.lineage_root


def test_all_closed_node_kinds_are_represented_where_expected():
    graph = build_graph()
    kinds = {node.kind for node in graph.nodes}
    assert NodeKind.CONTEXT in kinds
    assert NodeKind.VIEW in kinds
    assert NodeKind.FEATURE in kinds
    assert NodeKind.SOURCE_ARTIFACT in kinds
    assert NodeKind.TEMPORAL_ANCHOR in kinds
    assert NodeKind.EXTERNAL_CONTEXT_REFERENCE in kinds
    assert NodeKind.TREATMENT_DESCRIPTOR in kinds


def test_required_relation_families_exist():
    graph = build_graph()
    kinds = {edge.relation_kind for edge in graph.edges if edge.active}
    assert RelationKind.CONTEXT_COMPOSITION in kinds
    assert RelationKind.VIEW_COMPOSITION in kinds
    assert RelationKind.CROSS_VIEW_ALIGNMENT in kinds
    assert RelationKind.SEMANTIC_FAMILY in kinds


def test_graph_has_no_duplicate_identity():
    graph = build_graph()
    assert len({node.node_id for node in graph.nodes}) == len(graph.nodes)
    assert len({edge.edge_id for edge in graph.edges}) == len(graph.edges)


def test_treatment_descriptor_is_read_only():
    graph = build_graph()
    treatment = next(node for node in graph.nodes if node.kind == NodeKind.TREATMENT_DESCRIPTOR)
    assert dict(treatment.attributes)["read_only"] is True
