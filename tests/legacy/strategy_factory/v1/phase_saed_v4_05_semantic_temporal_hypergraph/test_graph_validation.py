from dataclasses import replace

import pytest

from .helpers import build_graph
from saed_v4_semantic_hypergraph.errors import GraphValidationError
from saed_v4_semantic_hypergraph.validation import validate_graph
from saed_v4_semantic_hypergraph.catalog import institutional_policy, institutional_registry


def validate(graph):
    return validate_graph(graph, institutional_registry(), institutional_policy())


def test_dangling_incidence_rejected():
    graph = build_graph()
    edge = replace(graph.edges[0], member_node_ids=graph.edges[0].member_node_ids + ("unknown_node",))
    with pytest.raises(GraphValidationError):
        validate(replace(graph, edges=(edge,) + graph.edges[1:]))


def test_duplicate_incidence_rejected():
    graph = build_graph()
    edge = graph.edges[0]
    edge = replace(edge, member_node_ids=edge.member_node_ids + (edge.member_node_ids[0],))
    with pytest.raises(GraphValidationError):
        validate(replace(graph, edges=(edge,) + graph.edges[1:]))


def test_node_hash_mismatch_rejected():
    graph = build_graph()
    node = replace(graph.nodes[0], node_hash="f" * 64)
    with pytest.raises(GraphValidationError):
        validate(replace(graph, nodes=(node,) + graph.nodes[1:]))


def test_edge_hash_mismatch_rejected():
    graph = build_graph()
    edge = replace(graph.edges[0], edge_hash="f" * 64)
    with pytest.raises(GraphValidationError):
        validate(replace(graph, edges=(edge,) + graph.edges[1:]))


def test_node_budget_fails_closed():
    graph = build_graph()
    policy = replace(institutional_policy(), maximum_nodes=1)
    with pytest.raises(GraphValidationError):
        validate_graph(graph, institutional_registry(), policy)


def test_graph_hash_mismatch_rejected():
    graph = build_graph()
    with pytest.raises(GraphValidationError):
        validate(replace(graph, graph_hash="0" * 64))


def test_graph_lineage_mismatch_rejected():
    graph = build_graph()
    with pytest.raises(GraphValidationError):
        validate(replace(graph, lineage_root="0" * 64))


def test_registry_identity_mismatch_rejected():
    graph = build_graph()
    with pytest.raises(GraphValidationError):
        validate(replace(graph, registry_hash="0" * 64))


def test_policy_identity_mismatch_rejected():
    graph = build_graph()
    with pytest.raises(GraphValidationError):
        validate(replace(graph, policy_hash="0" * 64))
