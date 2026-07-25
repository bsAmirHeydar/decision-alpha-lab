import copy,pytest,jsonschema

def test_unknown_field_rejected(load):
 s=load('schemas/legacy/strategy_factory/saed_v4_10/manual_program_source.schema.json');x=load('examples/legacy/strategy_factory/saed_v4_10/manual_doctrine_reference_v1.json');x['unknown']=1
 with pytest.raises(jsonschema.ValidationError):jsonschema.validate(x,s)
