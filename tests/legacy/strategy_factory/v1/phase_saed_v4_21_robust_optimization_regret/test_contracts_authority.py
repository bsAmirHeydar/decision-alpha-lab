import copy,pytest
from saed_v4_robust_optimization_regret.contracts import *
from saed_v4_robust_optimization_regret.authority import assert_operation,boundary_record,FORBIDDEN
from saed_v4_robust_optimization_regret.errors import ContractError,AuthorityError

def test_contracts_accept(config):
    UpstreamIntakeContract.from_mapping(config['upstream_intake']);AmbiguitySetContract.from_mapping(config['ambiguity']);ScenarioContract.from_mapping(config['scenario']);RobustOptimizationContract.from_mapping(config['optimization']);RegretContract.from_mapping(config['regret']);BaselineContract.from_mapping(config['baseline']);OptimizationBudget.from_mapping(config['budget'])
@pytest.mark.parametrize('key,cls',[('upstream_intake',UpstreamIntakeContract),('ambiguity',AmbiguitySetContract),('scenario',ScenarioContract),('optimization',RobustOptimizationContract),('regret',RegretContract),('baseline',BaselineContract),('budget',OptimizationBudget)])
def test_unknown_fields_rejected(config,key,cls):
    x=copy.deepcopy(config[key]);x['unknown']=1
    with pytest.raises(ContractError):cls.from_mapping(x)
@pytest.mark.parametrize('op',sorted(FORBIDDEN))
def test_forbidden_authority(op):
    with pytest.raises(AuthorityError):assert_operation(op)
def test_boundary_all_false():
    b=boundary_record();assert all(not b[k] for k in ['real_policy_value_claim_authority','production_treatment_selection_authority','risk_allocation_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])
