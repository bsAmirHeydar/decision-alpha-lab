import pytest
from strategy_factory_promotion_v3.conformance import generate_vectors,verify_vectors
from strategy_factory_promotion_v3.registry import registry,registry_snapshot,require_suite
from strategy_factory_promotion_v3.errors import PromotionError

def test_registry_has_seven_suites(): assert len(registry())==7
def test_registry_snapshot_is_stable(): assert registry_snapshot()==registry_snapshot()
def test_conformance_vectors_verify(): assert verify_vectors(generate_vectors())
def test_conformance_mutation_fails():
    v=generate_vectors(); v['version']='2.0.0'; assert not verify_vectors(v)
def test_unknown_suite_fails_closed():
    with pytest.raises(PromotionError): require_suite('missing')
