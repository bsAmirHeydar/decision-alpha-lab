import pytest
from strategy_factory_inference.examples import *
from strategy_factory_inference.models import FeatureOrder,FeatureBinding,TensorContract
from strategy_factory_inference.enums import TensorElementType

def test_reference_contracts_validate():
 FEATURE_ORDER.validate();PREPROCESSING.validate(4);CALIBRATION.validate();INPUT.validate();OUTPUT.validate()
 assert FEATURE_ORDER.bindings[0].feature_id=="ref.range_position"

def test_feature_order_is_exact_and_dense():
 bad=FeatureOrder(FEATURE_SCHEMA_HASH,(FeatureBinding("a","1",0),FeatureBinding("b","1",2))).with_hash()
 with pytest.raises(ValueError):bad.validate()

def test_static_tensor_shape_required():
 with pytest.raises(ValueError):TensorContract("features",TensorElementType.FLOAT32,(1,0)).validate()
