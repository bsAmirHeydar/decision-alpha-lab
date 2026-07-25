import pytest
from fp_i02_kernel.enums import RelationCode,WindowKind
from fp_i06_relations.registry import CATALOG,registry_hash,resolve_relation,supported_relations,validate_registry
from fp_i06_relations.errors import FPI06Error

def test_registry_contains_seven_canonical_relations():
    assert tuple(x.relation.value for x in CATALOG)==('AL','AN','LN','NA','NL','NN','WW')
    assert validate_registry()
def test_only_six_non_weekly_relations_supported_in_i06():
    assert tuple(x.relation.value for x in supported_relations())==('AL','AN','LN','NA','NL','NN')
    assert resolve_relation(RelationCode.WW).supported_in_phase is False
def test_relation_mapping_is_exact():
    expected={RelationCode.AL:(WindowKind.A,WindowKind.L),RelationCode.AN:(WindowKind.A,WindowKind.N),RelationCode.LN:(WindowKind.L,WindowKind.N),RelationCode.NA:(WindowKind.N,WindowKind.A),RelationCode.NL:(WindowKind.N,WindowKind.L),RelationCode.NN:(WindowKind.N,WindowKind.N)}
    assert {x.relation:(x.reference_kind,x.check_kind) for x in supported_relations()}==expected
def test_registry_hash_is_deterministic(): assert registry_hash()==registry_hash() and len(registry_hash())==64
def test_unknown_relation_fails_closed():
    with pytest.raises(FPI06Error):resolve_relation('ZZ')
