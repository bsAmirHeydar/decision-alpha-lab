import copy,pytest
from saed_v4_robust_optimization_regret.service import run_reference
from saed_v4_robust_optimization_regret.errors import BudgetError,ContractError

def test_budget_zero_hidden(config):assert config['budget']['max_hidden_evaluation_queries']==0 and config['budget']['protected_evidence_exposure_limit']==0
def test_budget_snapshot(result):
 b=result['budget_snapshot'];assert b['hidden_evaluation_queries']==0 and b['protected_evidence_exposures']==0 and b['objective_evaluations']>0
def test_candidate_budget_enforced(config,upstream,score):
 x=copy.deepcopy(config);x['budget']['max_candidates']=1
 with pytest.raises(BudgetError):run_reference(x,upstream,score)
def test_hidden_budget_rejected(config):
 from saed_v4_robust_optimization_regret.contracts import OptimizationBudget
 x=copy.deepcopy(config['budget']);x['max_hidden_evaluation_queries']=1
 with pytest.raises(ContractError):OptimizationBudget.from_mapping(x)
def test_runtime_flag_rejected(config):
 from saed_v4_robust_optimization_regret.contracts import RobustOptimizationContract
 x=copy.deepcopy(config['optimization']);x['runtime_executable']=True
 with pytest.raises(ContractError):RobustOptimizationContract.from_mapping(x)
