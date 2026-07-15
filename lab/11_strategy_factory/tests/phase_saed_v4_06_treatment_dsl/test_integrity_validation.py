from dataclasses import replace
import pytest
from helpers import build
from saed_v4_treatment_dsl.errors import IntegrityError
from saed_v4_treatment_dsl.integrity import build_integrity_receipt,verify_integrity
from saed_v4_treatment_dsl.validation import validate_package
from saed_v4_treatment_dsl.catalog import institutional_registry,institutional_policy
def test_integrity_receipt_verifies():
 p=build();r=build_integrity_receipt(p);assert verify_integrity(p,r)
@pytest.mark.parametrize('field',['package_hash','lineage_root','registry_hash','policy_hash','capability_profile_hash','source_graph_hash','source_handoff_hash'])
def test_tamper_rejected(field):
 p=build();bad=replace(p,**{field:'0'*64})
 with pytest.raises(IntegrityError):validate_package(bad,institutional_registry(),institutional_policy())
