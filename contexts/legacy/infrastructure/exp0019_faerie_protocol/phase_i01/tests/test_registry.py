import pytest
from fp_i01_compatibility.registry import CATALOG,default_registry,AdapterRegistry
from fp_i01_compatibility.errors import CompatibilityError

def test_catalog_has_exact_eight_adapters():
    assert len(CATALOG)==8 and len({x.key for x in CATALOG})==8

def test_registry_exact_resolution():
    r=default_registry();assert r.resolve('FP_CGT_TIME_ADAPTER@1.0.0').dependency_id=='CGT_TIME_CORE'
    with pytest.raises(CompatibilityError):r.resolve('FP_CGT_TIME_ADAPTER@latest')

def test_frozen_registry_rejects_mutation():
    r=default_registry()
    with pytest.raises(CompatibilityError,match='frozen'):r.register(CATALOG[0])

def test_all_descriptors_are_read_only_and_authority_free():
    assert all(not x.mutation_allowed and not x.authority for x in CATALOG)
