import pytest
from collections import defaultdict
from saed_v4_offline_policy_research.contracts import *
from saed_v4_offline_policy_research.behavior import estimate
from saed_v4_offline_policy_research.masks import compile_masks
from saed_v4_offline_policy_research.cql import train
from saed_v4_offline_policy_research.projection import project
from saed_v4_offline_policy_research.ope import evaluate
from saed_v4_offline_policy_research.trajectory import transitions

def bundle(config,dataset):
    actions=['skip','long','short'];b=estimate(dataset,BehaviorPolicyContract.from_mapping(config['behavior_policy_contract']),actions);m=compile_masks(dataset,actions);p=train(dataset,CQLContract.from_mapping(config['cql_contract']),actions,m);counts=defaultdict(lambda:defaultdict(int))
    for t in transitions(dataset):counts[t['state']][t['action']]+=1
    pp=project(p,b,m,counts,ProjectionContract.from_mapping(config['projection_contract']),actions);o=evaluate(dataset,b,pp,OPEContract.from_mapping(config['ope_contract']),actions);return actions,b,m,pp,o
def test_projection_passes(config,dataset):assert bundle(config,dataset)[3]['projection']['passed']
@pytest.mark.parametrize('state', ['flat','trend_up','trend_down','volatile'])
def test_projected_normalized(config,dataset,state):assert abs(sum(bundle(config,dataset)[3]['states'][state].values())-1)<1e-9
@pytest.mark.parametrize('estimator',['wis','pdis','fqe','doubly_robust'])
def test_ope_estimators(config,dataset,estimator):assert estimator in bundle(config,dataset)[4]['estimators']
@pytest.mark.parametrize('estimator',['wis','pdis','fqe','doubly_robust'])
def test_ope_intervals(config,dataset,estimator):
    ci=bundle(config,dataset)[4]['confidence_intervals'][estimator];assert ci['lower']<=ci['mean']<=ci['upper']
def test_ope_no_authority(config,dataset):
    o=bundle(config,dataset)[4];assert not o['promotion_authority'] and not o['synthetic_positive_evidence']
