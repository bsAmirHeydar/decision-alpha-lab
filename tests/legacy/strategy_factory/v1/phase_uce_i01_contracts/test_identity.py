import pytest
from strategy_factory_contracts_v3.enums import IdentityKind
from strategy_factory_contracts_v3.errors import IdentityError
from strategy_factory_contracts_v3.fixtures import golden_identity_cases
from strategy_factory_contracts_v3.identity import IdentityKey

def test_golden_context_occurrence_id():
    item=golden_identity_cases()[0]
    assert item.stable_id=="uce3_context_occurrence_06893bba7f56fb57"
    assert item.evidence_sha256=="d06964316802c451d64483ce799a2f40980b3e9b5be4275dc468d37ff638f175"

def test_identity_is_order_independent_for_dimension_mapping():
    left=IdentityKey(IdentityKind.TASK,"ucee.task","3.0.0","owner",{"b":2,"a":1})
    right=IdentityKey(IdentityKind.TASK,"ucee.task","3.0.0","owner",{"a":1,"b":2})
    assert left.stable_id==right.stable_id
    assert left.canonical_material==right.canonical_material

def test_mutable_identity_fields_fail_closed():
    with pytest.raises(IdentityError) as error:
        IdentityKey(IdentityKind.MODEL,"ucee.model","3.0.0","owner",{"created_at":1})
    assert error.value.code=="mutable_identity_dimension"
