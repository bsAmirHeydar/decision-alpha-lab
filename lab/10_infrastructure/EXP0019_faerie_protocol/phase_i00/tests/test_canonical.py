import math
import pytest

from fp_i00_governance.canonical import CanonicalizationError, canonical_json, canonical_sha256


def test_canonical_dict_order_is_irrelevant():
    assert canonical_json({"b": 2, "a": 1}) == canonical_json({"a": 1, "b": 2})
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})


def test_negative_zero_is_normalized():
    assert canonical_json({"x": -0.0}) == '{"x":0.0}'


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_non_finite_values_fail_closed(value):
    with pytest.raises(CanonicalizationError):
        canonical_json({"value": value})


def test_behavior_change_changes_hash():
    assert canonical_sha256({"policy": "M1_ONLY"}) != canonical_sha256({"policy": "TICK_FIRST"})
