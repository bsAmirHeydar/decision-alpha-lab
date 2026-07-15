import copy,pytest
from helpers import inputs
from saed_v4_execution_twin.models import ExecutionTwinProfile
from saed_v4_execution_twin.twin import build_execution_twin
from saed_v4_execution_twin.errors import BudgetError,ContractError

def test_source_row_budget_fails_closed():
    cube,handoff,m=inputs();m=copy.deepcopy(m);m['maximum_source_rows']=1
    with pytest.raises(BudgetError):build_execution_twin(cube,handoff,ExecutionTwinProfile.from_mapping(m))

def test_scenario_budget_fails_at_profile_contract():
    _,_,m=inputs();m=copy.deepcopy(m);m['maximum_scenarios']=1
    with pytest.raises(ContractError):ExecutionTwinProfile.from_mapping(m)

def test_disallowed_source_evidence_role_fails():
    cube,handoff,m=inputs();cube=copy.deepcopy(cube);cube['evidence_role']='protected_final'
    with pytest.raises(ContractError):build_execution_twin(cube,handoff,ExecutionTwinProfile.from_mapping(m))
