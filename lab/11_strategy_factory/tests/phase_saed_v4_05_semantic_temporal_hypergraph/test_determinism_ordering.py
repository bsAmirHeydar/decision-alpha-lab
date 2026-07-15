from dataclasses import replace

from helpers import build_graph, build_package
from saed_v4_semantic_hypergraph.builder import SemanticTemporalHypergraphBuilder
from saed_v4_semantic_hypergraph.catalog import institutional_policy, institutional_registry


def test_repeated_build_is_identical():
    package = build_package()
    registry = institutional_registry()
    policy = institutional_policy()
    builder = SemanticTemporalHypergraphBuilder()
    assert builder.build(package, registry, policy).graph_hash == builder.build(package, registry, policy).graph_hash


def test_registry_rule_order_is_not_semantic():
    package = build_package()
    registry = institutional_registry()
    policy = institutional_policy()
    left = build_graph(package, registry, policy)
    right = build_graph(package, replace(registry, rules=tuple(reversed(registry.rules))), policy)
    assert left.graph_hash == right.graph_hash


def test_registry_relation_order_is_not_semantic():
    package = build_package()
    registry = institutional_registry()
    left = build_graph(package, registry)
    right = build_graph(package, replace(registry, relations=tuple(reversed(registry.relations))))
    assert left.graph_hash == right.graph_hash


def test_irrelevant_request_id_is_not_semantic():
    assert build_graph(build_package(request_id="a")).graph_hash == build_graph(build_package(request_id="b")).graph_hash
