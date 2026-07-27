import pytest

from .helpers import build_graph
from saed_v4_semantic_hypergraph.canonical import stable_id
from saed_v4_semantic_hypergraph.enums import NodeKind, QueryDirection, RelationKind
from saed_v4_semantic_hypergraph.errors import QueryError
from saed_v4_semantic_hypergraph.models import GraphQuery
from saed_v4_semantic_hypergraph.projection import incidence_projection
from saed_v4_semantic_hypergraph.query import execute_query


def test_incidence_projection_shape():
    graph = build_graph()
    projection = incidence_projection(graph)
    assert len(projection.rows) == len(graph.edges)
    assert all(len(row) == len(graph.nodes) for row in projection.rows)
    assert projection.projection_hash


def test_incidence_projection_is_deterministic():
    graph = build_graph()
    assert incidence_projection(graph) == incidence_projection(graph)


def graph_query(graph, **overrides):
    context = next(node for node in graph.nodes if node.kind == NodeKind.CONTEXT)
    payload = dict(
        query_id=stable_id("query", context.node_id),
        seed_node_ids=(context.node_id,),
        relation_kinds=(RelationKind.CONTEXT_COMPOSITION,),
        node_kinds=(NodeKind.CONTEXT, NodeKind.VIEW),
        direction=QueryDirection.INCIDENT,
        maximum_hops=1,
        maximum_results=100,
        include_masked=False,
    )
    payload.update(overrides)
    return GraphQuery(**payload)


def test_bounded_query_returns_context_and_views():
    graph = build_graph()
    result = execute_query(graph, graph_query(graph))
    assert result.node_ids
    assert result.edge_ids
    assert not result.truncated


def test_query_result_is_deterministic():
    graph = build_graph()
    query = graph_query(graph)
    assert execute_query(graph, query) == execute_query(graph, query)


@pytest.mark.parametrize("hops", [-1, 9])
def test_query_hop_budget_enforced(hops):
    graph = build_graph()
    with pytest.raises(QueryError):
        execute_query(graph, graph_query(graph, maximum_hops=hops))


def test_unknown_query_seed_rejected():
    graph = build_graph()
    with pytest.raises(QueryError):
        execute_query(graph, graph_query(graph, seed_node_ids=("unknown",)))
