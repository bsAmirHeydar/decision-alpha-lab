import copy,pytest
from helpers import load
from saed_v4_treatment_dsl.errors import ContractError
from saed_v4_treatment_dsl.parser import parse_program

def test_parse_golden(): assert parse_program(load('golden_treatment_program_source.json')).program_name=='context.breakout.p3'
@pytest.mark.parametrize('field',['program_name','exact_version','descriptor_id','side_scope','components','constraints','states','transitions','semantic_labels','evidence_role','known_as_of','source_artifact_hash','limitations'])
def test_missing_top_level_field_rejected(field):
 d=load('golden_treatment_program_source.json');d.pop(field)
 with pytest.raises(ContractError):parse_program(d)
def test_unknown_top_level_field_rejected():
 d=load('golden_treatment_program_source.json');d['unknown']=1
 with pytest.raises(ContractError):parse_program(d)
def test_unknown_component_field_rejected():
 d=load('golden_treatment_program_source.json');d['components'][0]['unknown']=1
 with pytest.raises(ContractError):parse_program(d)
