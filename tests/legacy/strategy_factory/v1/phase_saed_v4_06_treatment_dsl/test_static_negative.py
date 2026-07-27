import pytest
from .helpers import load
from saed_v4_treatment_dsl.catalog import institutional_capability_profile,institutional_policy,institutional_registry
from saed_v4_treatment_dsl.parser import parse_program
from saed_v4_treatment_dsl.static_analysis import StaticTreatmentAnalyzer
CASES=[
('unknown_parameter.json','unknown_parameter'),('unknown_exact_primitive.json','unknown_exact_primitive'),('parameter_out_of_range.json','parameter_above_maximum'),('missing_capability_component.json','missing_required_component:capability'),('future_outcome_constraint.json','constraint_prohibited_future_or_outcome_ref'),('cyclic_state_machine.json','cyclic_management_state_machine'),('duplicate_singleton_kind.json','singleton_component_repeated:entry'),('mixed_system_action.json','action_must_be_isolated'),('duplicate_slot.json','duplicate_component_slot')]
@pytest.mark.parametrize('name,reason',CASES)
def test_negative_program_rejected(name,reason):
 s=parse_program(load('negative/'+name));r=StaticTreatmentAnalyzer().analyze(s,institutional_registry(),institutional_policy(),institutional_capability_profile());assert r.status.value=='rejected';assert reason in r.reason_codes
