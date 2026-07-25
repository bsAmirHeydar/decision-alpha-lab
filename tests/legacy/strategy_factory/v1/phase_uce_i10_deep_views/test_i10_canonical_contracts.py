import math
import pytest

from strategy_factory_deep_views_v3.canonical import canonical_json, canonical_sha256, stable_id
from strategy_factory_deep_views_v3.contracts import FusionPrediction
from strategy_factory_deep_views_v3.enums import FusionKind
from strategy_factory_deep_views_v3.errors import DeepViewError


def test_canonical_json_is_order_independent_and_rejects_nonfinite_values():
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})
    assert canonical_json({"minus_zero": -0.0}) == '{"minus_zero":0.0}'
    with pytest.raises(DeepViewError, match="NaN"):
        canonical_json({"bad": math.nan})


def test_stable_id_validates_prefix_and_digest_length():
    assert stable_id("uce_test", {"x": 1}).startswith("uce_test_")
    with pytest.raises(DeepViewError, match="prefix"):
        stable_id("bad-prefix", {"x": 1})
    with pytest.raises(DeepViewError, match="length"):
        stable_id("ok", {"x": 1}, length=2)


def test_fusion_prediction_rejects_non_normalized_weights_and_overlap():
    with pytest.raises(DeepViewError, match="sum to one"):
        FusionPrediction("p", "r", FusionKind.GATED, ("a",), (), {"a": 0.5}, 1.0, 0.0, False, "", "")
    with pytest.raises(DeepViewError, match="available and missing"):
        FusionPrediction("p", "r", FusionKind.GATED, ("a",), ("a",), {"a": 1.0}, 1.0, 0.0, False, "", "")
