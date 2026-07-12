from decimal import Decimal
import pytest
from strategy_factory_contracts_v3.codec import CanonicalDecimal,CanonicalScaledInteger,canonical_json
from strategy_factory_contracts_v3.errors import CanonicalizationError
from strategy_factory_contracts_v3.hashing import fnv1a64_hex

def test_canonical_object_order_and_ascii_escaping():
    assert canonical_json({"z":1,"a":"é","line":"x\ny"}) == r'{"a":"\u00e9","line":"x\ny","z":1}'

def test_fixed_scale_round_half_even_and_negative_zero():
    assert canonical_json(CanonicalDecimal("1.23445",4))=="1.2344"
    assert canonical_json(CanonicalDecimal("1.23455",4))=="1.2346"
    assert canonical_json(CanonicalDecimal("-0.00001",4))=="0.0000"
    assert canonical_json(CanonicalScaledInteger(1234567,5))=="12.34567"

def test_raw_binary_float_is_forbidden():
    with pytest.raises(CanonicalizationError) as error:canonical_json({"price":1.1})
    assert error.value.code=="raw_float_forbidden"

def test_known_fnv_utf8_vector():
    assert fnv1a64_hex(b"hello")=="a430d84680aabd0b"
