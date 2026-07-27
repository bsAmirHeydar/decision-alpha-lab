from dataclasses import replace

import pytest

from .helpers import build_graph, build_package
from saed_v4_semantic_hypergraph.errors import GraphValidationError


def test_tampered_source_package_hash_rejected():
    package = replace(build_package(), package_hash="0" * 64)
    with pytest.raises(GraphValidationError):
        build_graph(package)


def test_graph_binds_exact_source_package_hash():
    package = build_package()
    graph = build_graph(package)
    assert graph.source_package_id == package.package_id
    assert graph.source_package_hash == package.package_hash


def test_graph_binds_registry_and_policy_hashes():
    graph = build_graph()
    assert len(graph.registry_hash) == 64
    assert len(graph.policy_hash) == 64
