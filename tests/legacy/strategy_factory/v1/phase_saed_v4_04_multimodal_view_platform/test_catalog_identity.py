import pytest
from dataclasses import replace
from .helpers import service_and_specs,TWIN
from saed_v4_multimodal_views.enums import ViewKind
from saed_v4_multimodal_views.registry import ViewSpecificationRegistry
from saed_v4_multimodal_views.errors import RegistryError,AuthorityError

def test_catalog_has_ten_institutional_views():
 _,specs=service_and_specs();assert len(specs)==10;assert {s.kind for s in specs}==set(ViewKind)-{ViewKind.CUSTOM}
def test_spec_identity_is_stable_under_feature_order():
 _,specs=service_and_specs();s=specs[0];r=replace(s,features=tuple(reversed(s.features)));assert s.semantic_hash==r.semantic_hash;assert s.specification_id==r.specification_id
def test_exact_version_rebind_rejected():
 _,specs=service_and_specs();reg=ViewSpecificationRegistry();reg.register(specs[0])
 with pytest.raises(RegistryError):reg.register(replace(specs[0],description='changed'))
def test_duplicate_feature_rejected():
 _,specs=service_and_specs();s=specs[0]
 with pytest.raises(RegistryError):ViewSpecificationRegistry().register(replace(s,features=s.features+(s.features[0],)))
def test_forbidden_authority_rejected():
 _,specs=service_and_specs();s=replace(specs[0],authority=replace(specs[0].authority,train_model=True))
 with pytest.raises(AuthorityError):ViewSpecificationRegistry().register(s)
def test_all_specs_are_twin_bound():
 _,specs=service_and_specs();assert all(s.twin_id==TWIN for s in specs)
