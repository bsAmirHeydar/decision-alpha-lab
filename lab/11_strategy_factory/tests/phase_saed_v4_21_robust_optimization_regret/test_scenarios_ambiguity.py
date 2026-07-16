import copy,pytest
from saed_v4_robust_optimization_regret.scenarios import compile_scenarios
from saed_v4_robust_optimization_regret.ambiguity import compile_ambiguity_distributions
from saed_v4_robust_optimization_regret.errors import ScenarioError

def test_scenario_count(config,score):
    s=compile_scenarios(score,config['scenario'],config['ambiguity']);assert 7<=s['scenario_count']<=config['scenario']['max_scenarios'];assert not s['future_suffix_used'];assert not s['protected_evidence_used']
def test_scenario_determinism(config,score):assert compile_scenarios(score,config['scenario'],config['ambiguity'])==compile_scenarios(score,config['scenario'],config['ambiguity'])
def test_future_suffix_rejected(config,score):
    x=copy.deepcopy(score);x['future_suffix']=[999]
    with pytest.raises(ScenarioError):compile_scenarios(x,config['scenario'],config['ambiguity'])
def test_ambiguity_probabilities(config,score):
    s=compile_scenarios(score,config['scenario'],config['ambiguity']);a=compile_ambiguity_distributions(s,config['ambiguity'])
    assert a['distribution_count']>=2
    for d in a['distributions']:assert abs(sum(d['probabilities'])-1)<1e-12 and min(d['probabilities'])>=config['ambiguity']['probability_floor']-1e-12
@pytest.mark.parametrize('family',['scenario_convex_hull','wasserstein_l1','kl_ball_reference','moment_box','hybrid'])
def test_ambiguity_families(config,score,family):
    m=copy.deepcopy(config['ambiguity']);m['family']=family;s=compile_scenarios(score,config['scenario'],m);a=compile_ambiguity_distributions(s,m);assert a['family']==family
