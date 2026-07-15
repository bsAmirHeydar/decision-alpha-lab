import copy,pytest,jsonschema
from conftest import load

def test_unknown_profile_field_rejected():
    s=load('lab/11_strategy_factory/schemas/saed_v4_09/execution_twin_profile.schema.json');x=load('lab/11_strategy_factory/examples/saed_v4_09/execution_twin_profile.json');x['secret']=1
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(x,s)
