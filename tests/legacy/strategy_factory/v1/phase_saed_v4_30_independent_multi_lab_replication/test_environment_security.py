import copy,pytest
from saed_v4_independent_multi_lab_replication.environment import attest
from saed_v4_independent_multi_lab_replication.errors import SecurityError
FIELDS=["network_access","package_installation","interactive_shell","mutable_clock","shared_mutable_state"]
@pytest.mark.parametrize("field",FIELDS)
@pytest.mark.parametrize("lab_index",[0,1,2])
def test_environment_deny_controls_fail(inputs,result,field,lab_index):
 env=copy.deepcopy(inputs["environments"]); env[lab_index][field]=True
 with pytest.raises(SecurityError): attest(env,result["registry"])
@pytest.mark.parametrize("lab_index",[0,1,2])
def test_missing_environment_fails(inputs,result,lab_index):
 env=copy.deepcopy(inputs["environments"]); env.pop(lab_index)
 with pytest.raises(SecurityError): attest(env,result["registry"])
