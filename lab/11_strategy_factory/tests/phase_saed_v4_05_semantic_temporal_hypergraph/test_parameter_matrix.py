from dataclasses import replace

import pytest

from helpers import build_graph
from saed_v4_semantic_hypergraph.catalog import institutional_policy
from saed_v4_semantic_hypergraph.partitioning import deterministic_partition


@pytest.mark.parametrize("quality", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_quality_threshold_is_hash_bound(quality):
    policy = replace(institutional_policy(), minimum_feature_quality=quality)
    graph = build_graph(policy=policy)
    assert graph.policy_hash == policy.policy_hash


@pytest.mark.parametrize("partitions", [1, 3, 16, 64])
def test_partition_count_does_not_mutate_graph(partitions):
    graph = build_graph()
    before = graph.graph_hash
    deterministic_partition(graph, partitions)
    assert graph.graph_hash == before


@pytest.mark.parametrize("max_arity", [64, 128, 512, 1024])
def test_supported_arity_budgets(max_arity):
    policy = replace(institutional_policy(), maximum_edge_arity=max_arity)
    assert build_graph(policy=policy).graph_hash
