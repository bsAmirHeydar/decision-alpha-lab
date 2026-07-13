from dataclasses import dataclass
from enum import Enum

import pytest

from fp_i02_kernel.canonical import canonical_json, canonical_sha256, projection_hash, require_semver, require_sha256, semantic_hash, stable_id
from fp_i02_kernel.errors import FPI02Error


class E(str, Enum):
    B = "B"


@dataclass(frozen=True)
class D:
    z: float
    a: E


def test_canonical_mapping_order_and_dataclass_are_stable():
    assert canonical_json({"b": 2, "a": 1}) == canonical_json({"a": 1, "b": 2})
    assert canonical_sha256(D(0.0, E.B)) == canonical_sha256({"z": 0.0, "a": "B"})


def test_negative_zero_is_normalized():
    assert canonical_json(-0.0) == "0.0"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_values_fail_closed(value):
    with pytest.raises(FPI02Error, match="non-finite") as exc:
        canonical_json(value)
    assert exc.value.code == "FP_RC_NONFINITE_NUMBER"


def test_semantic_and_projection_domains_do_not_collide():
    value = {"x": 1}
    assert semantic_hash(value) != projection_hash(value)


def test_stable_id_repeats_and_width_is_validated():
    assert stable_id("FP", {"a": 1}) == stable_id("FP", {"a": 1})
    with pytest.raises(FPI02Error):
        stable_id("FP", {}, width=8)


def test_sha256_and_semver_validation():
    assert require_sha256("a" * 64, "x") == "a" * 64
    assert require_semver("1.2.3", "v") == "1.2.3"
    with pytest.raises(FPI02Error):
        require_sha256("A" * 64, "x")
    with pytest.raises(FPI02Error):
        require_semver("1.2", "v")
