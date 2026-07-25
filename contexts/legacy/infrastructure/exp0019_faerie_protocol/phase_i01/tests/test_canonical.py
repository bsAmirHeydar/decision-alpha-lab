import pytest
from fp_i01_compatibility.canonical import canonical_sha256,canonical_json,CanonicalizationError

def test_mapping_order_does_not_change_hash():
    assert canonical_sha256({'b':2,'a':1})==canonical_sha256({'a':1,'b':2})

def test_negative_zero_is_normalized():
    assert canonical_json({'x':-0.0})=='{"x":0.0}'

def test_non_finite_rejected():
    with pytest.raises(CanonicalizationError):canonical_json(float('nan'))
