import pytest
from strategy_factory_candidate import *
from strategy_factory_candidate.fixtures import ConfirmationMarket

def test_registry_compiles():
    r=build_fixture_registry();assert r.compiled;assert r.count(PolicyKind.ENTRY)==2;assert r.count(PolicyKind.STOP)==2;assert r.count(PolicyKind.EXIT)==2

def test_duplicate_rejected():
    r=PolicyRegistry();p=ConfirmationMarket();r.register(p)
    with pytest.raises(ValueError):r.register(p)

def test_registry_hash_stable():
    assert build_fixture_registry().registry_hash==build_fixture_registry().registry_hash
