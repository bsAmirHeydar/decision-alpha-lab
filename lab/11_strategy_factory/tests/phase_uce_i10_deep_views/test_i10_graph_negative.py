import pytest

from strategy_factory_deep_views_v3.errors import DeepViewError
from strategy_factory_deep_views_v3.golden import graph_spec
from strategy_factory_deep_views_v3.graph import build_graph_artifact, remove_edges


def _graph(edges):
    return build_graph_artifact(
        graph_spec(),
        "ctx",
        100,
        ("a", "b", "c"),
        (10, 20, 30),
        ((1.0, 0.0, 1.0), (2.0, 1.0, -1.0), (3.0, 2.0, 1.0)),
        edges,
    )


def test_graph_canonicalizes_edge_order_and_duplicate_edges():
    first = _graph(((1, 2), (0, 1), (1, 2)))
    second = _graph(((0, 1), (1, 2)))
    assert first.edges == second.edges
    assert first.topology_hash == second.topology_hash


def test_graph_rejects_self_loop_and_out_of_range_endpoint():
    with pytest.raises(DeepViewError, match="self-loop"):
        _graph(((0, 0),))
    with pytest.raises(DeepViewError, match="out of range"):
        _graph(((0, 3),))


def test_graph_ablation_edge_removal_is_canonical():
    assert remove_edges(((0, 1), (1, 2), (0, 2)), ((1, 2),)) == ((0, 1), (0, 2))
