import pytest,copy
from saed_v4_offline_policy_research.contracts import *
from saed_v4_offline_policy_research.authority import authority_boundary,assert_no_authority
CASES=[('upstream_intake',UpstreamIntakeContract),('logged_dataset_contract',LoggedDatasetContract),('action_space_contract',ActionSpaceContract),('reward_contract',RewardContract),('behavior_policy_contract',BehaviorPolicyContract),('support_contract',SupportContract),('cql_contract',CQLContract),('iql_contract',IQLContract),('sequence_policy_contract',SequencePolicyContract),('ope_contract',OPEContract),('projection_contract',ProjectionContract),('research_budget',ResearchBudget)]
@pytest.mark.parametrize('key,cls',CASES)
def test_contract_accepts_reference(config,key,cls):assert cls.from_mapping(config[key])
@pytest.mark.parametrize('key,cls',CASES)
def test_contract_rejects_unknown(config,key,cls):
    x=copy.deepcopy(config[key]);x['unknown']=1
    with pytest.raises(ContractError):cls.from_mapping(x)
def test_authority_all_denied():
    a=authority_boundary();assert_no_authority(a);assert not any(a['authority'].values()) and a['offline_only']
@pytest.mark.parametrize('field',list(authority_boundary()['authority']))
def test_authority_escalation_rejected(field):
    a=authority_boundary();a['authority'][field]=True
    with pytest.raises(Exception):assert_no_authority(a)
