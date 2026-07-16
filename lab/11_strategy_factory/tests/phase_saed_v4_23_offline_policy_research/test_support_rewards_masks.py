import pytest
from collections import defaultdict
from saed_v4_offline_policy_research.contracts import *
from saed_v4_offline_policy_research.rewards import audit
from saed_v4_offline_policy_research.behavior import estimate
from saed_v4_offline_policy_research.masks import compile_masks
from saed_v4_offline_policy_research.policies import baseline_from_document
from saed_v4_offline_policy_research.support import diagnose

def setup(config,dataset,baseline):
    actions=['skip','long','short'];b=estimate(dataset,BehaviorPolicyContract.from_mapping(config['behavior_policy_contract']),actions);p=baseline_from_document(baseline);return actions,b,p

def test_reward_audit(config,dataset):assert audit(dataset,RewardContract.from_mapping(config['reward_contract']))['passed']
def test_masks(dataset):
    m=compile_masks(dataset,['skip','long','short']);assert m['all_states_have_safe_action']
@pytest.mark.parametrize('state', ['flat','trend_up','trend_down','volatile'])
def test_mask_has_skip(dataset,state):assert compile_masks(dataset,['skip','long','short'])['states'][state]['skip']
def test_support_baseline_passes(config,dataset,baseline):
    actions,b,p=setup(config,dataset,baseline);r=diagnose(dataset,b,p,SupportContract.from_mapping(config['support_contract']),actions);assert r['passed'] and r['effective_sample_size']>0
@pytest.mark.parametrize('action', ['skip','long','short'])
def test_reward_components_exist(config,dataset,action):
    rows=[s for e in dataset['episodes'] for s in e['steps'] if s['action']==action];assert rows and all(set(r['reward_components'])=={'gross_return','execution_cost','risk_penalty'} for r in rows)
@pytest.mark.parametrize('state', ['flat','trend_up','trend_down','volatile'])
def test_baseline_normalized(config,dataset,baseline,state):
    _,_,p=setup(config,dataset,baseline);assert abs(sum(p['states'][state].values())-1)<1e-9
