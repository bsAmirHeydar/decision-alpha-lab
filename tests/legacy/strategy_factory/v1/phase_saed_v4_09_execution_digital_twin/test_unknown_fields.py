import copy,pytest,jsonschema
from .conftest import load

def test_unknown_profile_field_rejected():
    s=load('schemas/legacy/strategy_factory/saed_v4_09/execution_twin_profile.schema.json');x=load('examples/legacy/strategy_factory/saed_v4_09/execution_twin_profile.json');x['secret']=1
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(x,s)
