from dataclasses import replace

import pytest

from helpers import build_graph, build_package
from saed_v4_semantic_hypergraph.catalog import institutional_policy
from saed_v4_semantic_hypergraph.errors import GraphValidationError


def test_missing_required_view_rejected_before_graph_construction():
    package = build_package(include_views=("price_view", "structure_view"))
    with pytest.raises(GraphValidationError):
        build_graph(package)


def test_graph_budget_rejected():
    policy = replace(institutional_policy(), maximum_edges=2)
    with pytest.raises(Exception, match="edge budget exceeded"):
        build_graph(policy=policy)


def test_degraded_package_policy_can_be_strict():
    package = build_package()
    strict = replace(institutional_policy(), allow_degraded_views=False)
    # Golden package is compatible and remains admissible under the stricter policy.
    assert build_graph(package, policy=strict).graph_hash


def test_missing_execution_evidence_is_unsupported_not_imputed():
    from helpers import golden_sources
    from saed_v4_semantic_hypergraph.enums import GraphStatus

    sources = tuple(item for item in golden_sources() if item.namespace != "execution")
    package = build_package(sources)
    graph = build_graph(package)
    assert graph.status == GraphStatus.UNSUPPORTED
    assert graph.support.missing_required_relations
    assert any(node.masked for node in graph.nodes)


def test_strict_policy_rejects_degraded_source_package():
    from helpers import golden_sources

    sources = tuple(item for item in golden_sources() if item.namespace != "execution")
    package = build_package(sources)
    strict = replace(institutional_policy(), allow_degraded_views=False)
    with pytest.raises(GraphValidationError):
        build_graph(package, policy=strict)
