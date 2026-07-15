import copy,pytest,jsonschema

def test_unknown_field_rejected(load):
 s=load('lab/11_strategy_factory/schemas/saed_v4_10/manual_program_source.schema.json');x=load('lab/11_strategy_factory/examples/saed_v4_10/manual_doctrine_reference_v1.json');x['unknown']=1
 with pytest.raises(jsonschema.ValidationError):jsonschema.validate(x,s)
