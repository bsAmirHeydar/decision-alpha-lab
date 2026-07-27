import copy
from .helpers import inputs,built
from saed_v4_execution_twin.models import ExecutionTwinProfile
from saed_v4_execution_twin.twin import build_execution_twin

def test_source_inputs_are_not_mutated():
    cube,handoff,m=inputs();before=(copy.deepcopy(cube),copy.deepcopy(handoff),copy.deepcopy(m));build_execution_twin(cube,handoff,ExecutionTwinProfile.from_mapping(m));assert (cube,handoff,m)==before

def test_source_row_order_does_not_change_output():
    cube,handoff,m=inputs();p=ExecutionTwinProfile.from_mapping(m);a=build_execution_twin(cube,handoff,p);cube2=copy.deepcopy(cube);cube2['rows']=list(reversed(cube2['rows']));b=build_execution_twin(cube2,handoff,p);assert a==b

def test_scenario_input_order_does_not_change_output():
    cube,handoff,m=inputs();a=build_execution_twin(cube,handoff,ExecutionTwinProfile.from_mapping(m));m2=copy.deepcopy(m);m2['scenarios']=list(reversed(m2['scenarios']));b=build_execution_twin(cube,handoff,ExecutionTwinProfile.from_mapping(m2));assert a==b

def test_two_independent_builds_are_byte_semantically_equal():
    cube,handoff,p,t=built();assert build_execution_twin(copy.deepcopy(cube),copy.deepcopy(handoff),p)==t
