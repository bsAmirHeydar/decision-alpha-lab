from dataclasses import replace

import pytest

from .helpers import build_graph
from saed_v4_semantic_hypergraph.enums import EvidenceRole
from saed_v4_semantic_hypergraph.errors import GraphValidationError, TemporalBoundaryError
from saed_v4_semantic_hypergraph.validation import validate_graph
from saed_v4_semantic_hypergraph.catalog import institutional_policy, institutional_registry


def test_all_nodes_are_inside_graph_boundary():
    graph = build_graph()
    assert all(node.event_time <= graph.event_as_of for node in graph.nodes)
    assert all(node.known_time <= graph.known_as_of for node in graph.nodes)


def test_future_node_is_rejected():
    graph = build_graph()
    node = replace(graph.nodes[0], event_time="2027-01-01T00:00:00Z")
    mutated = replace(graph, nodes=(node,) + graph.nodes[1:])
    with pytest.raises(TemporalBoundaryError):
        validate_graph(mutated, institutional_registry(), institutional_policy())


def test_cross_role_node_is_rejected():
    graph = build_graph()
    node = replace(graph.nodes[0], evidence_role=EvidenceRole.LOCKED_FINAL)
    mutated = replace(graph, nodes=(node,) + graph.nodes[1:])
    with pytest.raises(GraphValidationError):
        validate_graph(mutated, institutional_registry(), institutional_policy())


def test_edge_interval_cannot_invert():
    graph = build_graph()
    edge = replace(graph.edges[0], event_time_start=graph.known_as_of, event_time_end=graph.event_as_of)
    mutated = replace(graph, edges=(edge,) + graph.edges[1:])
    with pytest.raises(TemporalBoundaryError):
        validate_graph(mutated, institutional_registry(), institutional_policy())
