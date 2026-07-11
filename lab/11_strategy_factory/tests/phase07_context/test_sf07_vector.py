import pytest
from strategy_factory_context.descriptor import FeatureVectorSchema,VectorField
from strategy_factory_context.enums import MissingPolicy
from strategy_factory_contracts.enums import FeatureType
from strategy_factory_context.registry import FeatureGraphError
from sf07_helpers import registry,vector_schema

def test_vector_schema_validates_against_registry():registry().validate_vector_fields(vector_schema().fields)
def test_vector_type_mismatch_rejected():
    bad=FeatureVectorSchema('bad','1.0.0',(VectorField('event_direction',FeatureType.DOUBLE,MissingPolicy.FAIL,0.0),))
    with pytest.raises(FeatureGraphError):registry().validate_vector_fields(bad.fields)
def test_vector_hash_stable():assert vector_schema().schema_hash==vector_schema().schema_hash
