import pytest

from helpers import build_graph
from saed_v4_semantic_hypergraph.partitioning import deterministic_partition
from saed_v4_semantic_hypergraph.telemetry import build_telemetry


@pytest.mark.parametrize("count", [1, 2, 4, 16, 31])
def test_partition_assignments_are_bounded(count):
    graph = build_graph()
    manifest = deterministic_partition(graph, count)
    assert all(0 <= partition < count for _, partition in manifest.node_partitions)
    assert all(0 <= partition < count for _, partition in manifest.edge_partitions)


def test_partitioning_is_deterministic():
    graph = build_graph()
    assert deterministic_partition(graph, 16) == deterministic_partition(graph, 16)


def test_telemetry_contains_no_authority_violation():
    telemetry = build_telemetry(build_graph())
    assert telemetry.deterministic is True
    assert telemetry.authority_violation_count == 0
    assert telemetry.telemetry_hash
