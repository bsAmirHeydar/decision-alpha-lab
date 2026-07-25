import copy,pytest
from saed_v4_independent_multi_lab_replication.registry import register_labs
from saed_v4_independent_multi_lab_replication.errors import EligibilityError
DIMS=["organization_id","operator_id","signing_key_id","environment_id","infrastructure_id","mutable_state_group"]
@pytest.mark.parametrize("dimension",DIMS)
def test_shared_independence_dimension_fails(inputs,result,dimension):
 labs=copy.deepcopy(inputs["labs"]); labs[1][dimension]=labs[0][dimension]
 with pytest.raises(EligibilityError): register_labs(labs,result["protocol"])
@pytest.mark.parametrize("relation",["author","sponsor","same_team","affiliate","unknown","consultant"])
def test_originator_relation_fails(inputs,result,relation):
 labs=copy.deepcopy(inputs["labs"]); labs[0]["originator_relation"]=relation
 with pytest.raises(EligibilityError): register_labs(labs,result["protocol"])
@pytest.mark.parametrize("count",[0,1,2])
def test_minimum_lab_count_fails(inputs,result,count):
 with pytest.raises(Exception): register_labs(copy.deepcopy(inputs["labs"][:count]),result["protocol"])
