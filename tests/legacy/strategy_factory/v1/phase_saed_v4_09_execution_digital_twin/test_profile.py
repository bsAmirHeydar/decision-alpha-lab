import copy, pytest
from helpers import inputs
from saed_v4_execution_twin.models import ExecutionTwinProfile
from saed_v4_execution_twin.errors import ContractError

def test_profile_identity_is_deterministic():
    _,_,m=inputs();a=ExecutionTwinProfile.from_mapping(m);b=ExecutionTwinProfile.from_mapping(copy.deepcopy(m))
    assert a.profile_id==b.profile_id and a.profile_hash==b.profile_hash

@pytest.mark.parametrize('mutator',[lambda x:x.update(synthetic_watermark=False),lambda x:x['latency'].update(submit_ms=-1),lambda x:x['fill_hazard'].update(base_probability=1.1),lambda x:x.update(allowed_evidence_roles=['oracle'])])
def test_invalid_profiles_fail_closed(mutator):
    _,_,m=inputs();m=copy.deepcopy(m);mutator(m)
    with pytest.raises(ContractError):ExecutionTwinProfile.from_mapping(m)

def test_duplicate_scenario_fails():
    _,_,m=inputs();m=copy.deepcopy(m);m['scenarios'].append(copy.deepcopy(m['scenarios'][0]))
    with pytest.raises(ContractError):ExecutionTwinProfile.from_mapping(m)
