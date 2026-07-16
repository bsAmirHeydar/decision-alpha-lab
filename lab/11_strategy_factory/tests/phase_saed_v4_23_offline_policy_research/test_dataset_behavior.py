import copy,pytest
from saed_v4_offline_policy_research.contracts import *
from saed_v4_offline_policy_research.trajectory import validate_dataset,transitions
from saed_v4_offline_policy_research.behavior import estimate
from saed_v4_offline_policy_research.errors import DatasetError

def contracts(config):return LoggedDatasetContract.from_mapping(config['logged_dataset_contract']),ActionSpaceContract.from_mapping(config['action_space_contract']),RewardContract.from_mapping(config['reward_contract'])
def test_dataset_reference(config,dataset):
    s=validate_dataset(dataset,*contracts(config));assert s['episode_count']==24 and s['step_count']==192 and len(s['states'])==4
@pytest.mark.parametrize('mutation',range(12))
def test_dataset_mutations_fail(config,dataset,mutation):
    x=copy.deepcopy(dataset);st=x['episodes'][0]['steps'][0]
    if mutation==0:st['behavior_prob']=0
    elif mutation==1:st['known_at']='2027-01-01T00:00:00Z'
    elif mutation==2:st['action']='hold'
    elif mutation==3:st['allowed_actions']=['long']
    elif mutation==4:st['reward']+=1
    elif mutation==5:st['reward_components']['execution_cost']=0.1
    elif mutation==6:st['reward_components']['foo']=0
    elif mutation==7:st['t']=-1;x['episodes'][0]['steps'][1]['t']=-2
    elif mutation==8:x['episodes'][0]['steps'][-1]['done']=False
    elif mutation==9:x['episodes']=x['episodes'][:2]
    elif mutation==10:st['state']=''
    else:x['extra']=1
    with pytest.raises(DatasetError):validate_dataset(x,*contracts(config))
def test_behavior_policy(config,dataset):
    c=BehaviorPolicyContract.from_mapping(config['behavior_policy_contract']);p=estimate(dataset,c,['skip','long','short']);assert all(abs(sum(v.values())-1)<1e-9 for v in p['states'].values())
@pytest.mark.parametrize('state', ['flat','trend_up','trend_down','volatile'])
def test_behavior_has_all_actions(config,dataset,state):
    p=estimate(dataset,BehaviorPolicyContract.from_mapping(config['behavior_policy_contract']),['skip','long','short']);assert set(p['states'][state])=={'skip','long','short'}
