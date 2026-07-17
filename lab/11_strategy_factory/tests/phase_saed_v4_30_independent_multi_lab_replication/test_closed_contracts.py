import copy,pytest
from saed_v4_independent_multi_lab_replication.errors import ContractError
from saed_v4_independent_multi_lab_replication.protocol import freeze_protocol
from saed_v4_independent_multi_lab_replication.package import build_package_identity
from saed_v4_independent_multi_lab_replication.upstream import verify_upstream
from saed_v4_independent_multi_lab_replication.registry import register_labs
from saed_v4_independent_multi_lab_replication.environment import attest

@pytest.mark.parametrize("field",["x","future_value","promotion","runtime","order","secret","debug","retry","raw_rows","hidden_labels"])
def test_protocol_unknown_fields_fail(inputs,field):
 v=copy.deepcopy(inputs["protocol"]); v[field]=1
 with pytest.raises(ContractError): freeze_protocol(v)
@pytest.mark.parametrize("field",["x","token","raw_dataset","hidden_label","future_metric","authority","signature_override","adaptive_retry"])
def test_package_unknown_fields_fail(inputs,result,field):
 v=copy.deepcopy(inputs["package"]); v[field]=1
 with pytest.raises(ContractError): build_package_identity(v,result["upstream"],result["protocol"])
@pytest.mark.parametrize("field",["x","candidate","token","raw_rows","operator_override","future_data"])
def test_upstream_unknown_fields_fail(inputs,field):
 v=copy.deepcopy(inputs["upstream"]); v[field]=1
 with pytest.raises(ContractError): verify_upstream(v)
@pytest.mark.parametrize("field",["x","shared_key","retry_budget","promotion_vote","hidden_access","future_suffix","order_permission","runtime_permission"])
def test_lab_unknown_fields_fail(inputs,result,field):
 labs=copy.deepcopy(inputs["labs"]); labs[0][field]=1
 with pytest.raises(ContractError): register_labs(labs,result["protocol"])
@pytest.mark.parametrize("field",["x","network_rule","secret","mutable_dependency","future_time","debug_port","runtime_authority","execution_authority"])
def test_environment_unknown_fields_fail(inputs,result,field):
 env=copy.deepcopy(inputs["environments"]); env[0][field]=1
 with pytest.raises(ContractError): attest(env,result["registry"])
