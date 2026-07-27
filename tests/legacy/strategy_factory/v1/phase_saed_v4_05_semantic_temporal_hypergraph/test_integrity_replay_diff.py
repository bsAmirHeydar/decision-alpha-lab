from .helpers import build_graph, build_package, changed_sources
from saed_v4_semantic_hypergraph.diff import diff_graphs
from saed_v4_semantic_hypergraph.integrity import build_integrity_receipt, verify_integrity
from saed_v4_semantic_hypergraph.replay import replay_graph
from saed_v4_semantic_hypergraph.catalog import institutional_policy, institutional_registry


def test_integrity_receipt_verifies():
    graph = build_graph()
    receipt = build_integrity_receipt(graph)
    assert receipt.status == "pass"
    assert verify_integrity(graph, receipt)


def test_deterministic_replay_passes():
    package = build_package()
    graph = build_graph(package)
    receipt = replay_graph(
        expected=graph,
        package=package,
        registry=institutional_registry(),
        policy=institutional_policy(),
    )
    assert receipt.status == "pass"
    assert receipt.expected_graph_hash == receipt.observed_graph_hash


def test_semantic_diff_detects_changed_source():
    left = build_graph()
    right = build_graph(build_package(changed_sources("projection", "quote_rate", 43.0)))
    diff = diff_graphs(left, right)
    assert diff.left_graph_hash != diff.right_graph_hash
    assert diff.added_node_ids or diff.removed_node_ids or diff.changed_node_ids
    assert diff.added_edge_ids or diff.removed_edge_ids or diff.changed_edge_ids


def test_identical_graph_diff_is_empty():
    graph = build_graph()
    diff = diff_graphs(graph, graph)
    assert not diff.added_node_ids
    assert not diff.changed_edge_ids
    assert not diff.status_changed
