import pytest
from strategy_factory_policy_v3.registry import registry,registry_snapshot,require_node
from strategy_factory_policy_v3.conformance import generate_vectors,verify_vectors
from strategy_factory_policy_v3.enums import NodeKind
from strategy_factory_policy_v3.errors import PolicyError

def test_registry_has_fourteen_node_kinds(): assert len(registry())==14
def test_registry_has_no_runtime_authority(): assert not any(x.runtime_authority for x in registry())
def test_registry_snapshot_stable(): assert registry_snapshot()==registry_snapshot()
def test_every_enum_node_registered(): assert {x.node_kind for x in registry()}=={x.value for x in NodeKind}
def test_require_node(): assert require_node('model_filter').authority=='model'
def test_unknown_node_fails_closed():
    with pytest.raises(PolicyError):require_node('unknown')
def test_conformance_vectors_verify(): assert verify_vectors(generate_vectors())
def test_mutated_vector_fails():
    v=generate_vectors();v['status']='rejected';assert not verify_vectors(v)
