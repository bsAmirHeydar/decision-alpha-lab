import pytest
from strategy_factory.context import FeatureVectorSchema, FeatureVectorError


def test_vector_schema_encodes_in_order():
    schema = FeatureVectorSchema(("b", "a"), (0.0, 0.0), "1")
    assert schema.encode({"a": 1, "b": 2}) == (2.0, 1.0)


def test_vector_schema_default_and_strict():
    schema = FeatureVectorSchema(("x",), (7.0,), "1")
    assert schema.encode({}) == (7.0,)
    with pytest.raises(FeatureVectorError):
        schema.encode({"x": None}, strict=True)
