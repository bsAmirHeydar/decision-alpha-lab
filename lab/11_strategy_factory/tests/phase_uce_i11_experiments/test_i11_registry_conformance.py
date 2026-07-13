import json

import pytest

from strategy_factory_experiments_v3.conformance import generate_vectors, verify_vectors
from strategy_factory_experiments_v3.errors import ExperimentError
from strategy_factory_experiments_v3.registry import CATALOG, SearchRegistry


def test_search_registry_is_exact_versioned_and_frozen():
    registry = SearchRegistry().freeze()
    snapshot = registry.snapshot()
    assert snapshot.frozen
    assert len(snapshot.descriptors) == 10
    assert len({descriptor.key for descriptor in snapshot.descriptors}) == 10
    assert sum(descriptor.native for descriptor in snapshot.descriptors) == 9
    assert registry.resolve_exact("uce.search.grid@1.0.0").native


def test_frozen_registry_rejects_mutation():
    registry = SearchRegistry().freeze()
    with pytest.raises(ExperimentError, match="search_registry_frozen"):
        registry.register(CATALOG[0])


def test_conformance_vectors_are_self_consistent_and_tamper_evident():
    vectors = generate_vectors()
    assert verify_vectors(vectors)
    tampered = dict(vectors)
    tampered["node_count"] += 1
    assert not verify_vectors(tampered)


def test_conformance_vector_json_roundtrip():
    vectors = generate_vectors()
    assert verify_vectors(json.loads(json.dumps(vectors, sort_keys=True)))
