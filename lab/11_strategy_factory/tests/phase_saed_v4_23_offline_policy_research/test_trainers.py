import pytest
from collections import defaultdict
from saed_v4_offline_policy_research.contracts import *
from saed_v4_offline_policy_research.behavior import estimate
from saed_v4_offline_policy_research.masks import compile_masks
from saed_v4_offline_policy_research.cql import train as cql
from saed_v4_offline_policy_research.iql import train as iql
from saed_v4_offline_policy_research.sequence_policy import train as seq

def trained(config,dataset):
    a=['skip','long','short'];m=compile_masks(dataset,a);b=estimate(dataset,BehaviorPolicyContract.from_mapping(config['behavior_policy_contract']),a)
    return [cql(dataset,CQLContract.from_mapping(config['cql_contract']),a,m),iql(dataset,b,IQLContract.from_mapping(config['iql_contract']),a,m),seq(dataset,b,SequencePolicyContract.from_mapping(config['sequence_policy_contract']),a,m)]
def test_all_trainers(config,dataset):assert len(trained(config,dataset))==3
@pytest.mark.parametrize('idx',range(3))
def test_policy_research_only(config,dataset,idx):
    p=trained(config,dataset)[idx];assert p['research_only'] and not p['runtime_executable'] and not p['promotion_eligible']
@pytest.mark.parametrize('idx,state',[(i,s) for i in range(3) for s in ['flat','trend_up','trend_down','volatile']])
def test_policy_normalized(config,dataset,idx,state):assert abs(sum(trained(config,dataset)[idx]['states'][state].values())-1)<1e-9
@pytest.mark.parametrize('idx',range(3))
def test_policy_deterministic(config,dataset,idx):assert trained(config,dataset)[idx]['policy_hash']==trained(config,dataset)[idx]['policy_hash']
