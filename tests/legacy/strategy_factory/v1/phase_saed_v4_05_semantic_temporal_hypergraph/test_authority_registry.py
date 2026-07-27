from dataclasses import replace

import pytest

from .helpers import build_graph
from saed_v4_semantic_hypergraph.catalog import institutional_registry
from saed_v4_semantic_hypergraph.errors import AuthorityError, RegistryError
from saed_v4_semantic_hypergraph.models import Selector
from saed_v4_semantic_hypergraph.registry import validate_registry


@pytest.mark.parametrize(
    "field",
    [
        "mutate_ucee_truth",
        "mutate_view_artifacts",
        "infer_canonical_relations",
        "fit_adaptive_statistics",
        "learn_edges",
        "train_model",
        "generate_treatment",
        "select_treatment",
        "allocate_risk",
        "activate_runtime",
        "send_order",
        "network_access",
    ],
)
def test_forbidden_authority_fails_closed(field):
    registry = institutional_registry()
    boundary = replace(registry.authority, **{field: True})
    with pytest.raises(AuthorityError):
        validate_registry(replace(registry, authority=boundary))


def test_duplicate_relation_definition_rejected():
    registry = institutional_registry()
    with pytest.raises(RegistryError):
        validate_registry(replace(registry, relations=registry.relations + (registry.relations[0],)))


def test_prohibited_outcome_selector_rejected():
    registry = institutional_registry()
    rule = replace(registry.rules[0], selectors=(Selector("price_view", "future_outcome"),))
    with pytest.raises(RegistryError):
        validate_registry(replace(registry, rules=(rule,) + registry.rules[1:]))


def test_registry_is_hash_stable():
    registry = institutional_registry()
    assert registry.registry_id.startswith("semreg_")
    assert len(registry.registry_hash) == 64
