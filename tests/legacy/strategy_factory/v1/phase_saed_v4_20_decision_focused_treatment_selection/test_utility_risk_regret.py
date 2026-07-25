import pytest
from saed_v4_decision_focused_treatment_selection.contracts import UtilityContract,RiskContract,ConstraintContract
from saed_v4_decision_focused_treatment_selection.utilities import compute_utility,path_statistics
from saed_v4_decision_focused_treatment_selection.risk import compute_risk_adjusted_scores,constraint_risk_failures
from saed_v4_decision_focused_treatment_selection.regret import scenario_regret_matrix
from saed_v4_decision_focused_treatment_selection.numerics import cvar_lower,max_drawdown,softmax,entropy,quantile

def test_path_statistics_are_deterministic():
 s=path_statistics([1,-1,2,-0.5]);assert s['path_count']==4;assert s['max_drawdown']>=1;assert s['tail_loss_probability']==0.25

def test_utility_contains_all_penalties(config,outcomes):
 u=UtilityContract.from_mapping(config['utility']);t=next(x for x in config['treatment_universe']['treatments'] if x['treatment_id']=='T_BALANCED');r=compute_utility(outcomes['T_BALANCED'],t,u);assert set(['expected_utility','raw_utility','tail_cvar','tail_loss_probability','max_drawdown'])<=set(r)

def test_risk_score_ordering(config,outcomes):
 u=UtilityContract.from_mapping(config['utility']);r=RiskContract.from_mapping(config['risk']);t=next(x for x in config['treatment_universe']['treatments'] if x['treatment_id']=='T_BALANCED');x=compute_risk_adjusted_scores(outcomes['T_BALANCED'],compute_utility(outcomes['T_BALANCED'],t,u),r);assert x['lower_confidence_utility']<=x['mean_utility']<=x['upper_confidence_utility'];assert x['robust_utility']<=x['lower_confidence_utility']

def test_constraint_risk_failures(config):
 c=ConstraintContract.from_mapping(config['constraints']);assert set(constraint_risk_failures({'tail_loss_probability':1.0,'max_drawdown':99.0},c))=={'tail_loss_probability','maximum_drawdown'}

def test_regret_matrix_has_zero_for_oracle():
 rows=[{'treatment_id':'A','scenario_utilities':{'s1':1,'s2':0}},{'treatment_id':'B','scenario_utilities':{'s1':0,'s2':2}}];m=scenario_regret_matrix(rows);assert m['scenarios'][0]['regret_by_treatment']['A']==0;assert m['scenarios'][1]['regret_by_treatment']['B']==0
@pytest.mark.parametrize('xs,q,expected',[([1,2,3],0,1),([1,2,3],1,3),([0,10],0.5,5)])
def test_quantile(xs,q,expected):assert quantile(xs,q)==expected

def test_softmax_and_entropy():
 p=softmax([1,2,3]);assert abs(sum(p)-1)<1e-12;assert entropy(p)>0

def test_cvar_and_drawdown():assert cvar_lower([-2,-1,1,2],0.5)==-1.5 and max_drawdown([1,-3,1])==3
