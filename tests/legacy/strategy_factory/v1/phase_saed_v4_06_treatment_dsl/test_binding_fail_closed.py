import pytest
from helpers import build,load,graph,handoff
from saed_v4_treatment_dsl.catalog import institutional_capability_profile,institutional_policy,institutional_registry
from saed_v4_treatment_dsl.errors import BindingError,TemporalBoundaryError
from saed_v4_treatment_dsl.parser import parse_program
from saed_v4_treatment_dsl.service import TreatmentDslService

def call(name):
 s=parse_program(load('negative/'+name));skip=parse_program(load('system_skip_program_source.json'));ab=parse_program(load('system_abstain_program_source.json'))
 return TreatmentDslService().build_package(graph=graph(),handoff=handoff(),registry=institutional_registry(),policy=institutional_policy(),capability_profile=institutional_capability_profile(),sources=(s,skip,ab))
@pytest.mark.parametrize('name,error',[('unknown_descriptor_binding.json',BindingError),('descriptor_label_mismatch.json',BindingError),('cross_role_binding.json',TemporalBoundaryError)])
def test_binding_negative(name,error):
 with pytest.raises(error): call(name)
def test_masked_descriptor_rejected():
 g=graph();n=next(x for x in g['nodes'] if x['kind']=='treatment_descriptor');n['masked']=True
 with pytest.raises(BindingError):build(g=g)
def test_mutable_descriptor_rejected():
 g=graph();n=next(x for x in g['nodes'] if x['kind']=='treatment_descriptor');n['attributes']['read_only']=False
 with pytest.raises(BindingError):build(g=g)
