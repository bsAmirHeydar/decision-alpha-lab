import copy,pytest
from saed_v4_generative_path_stress_lab.contracts import RolloutBudget,GeneratorProgramContract,ExploitabilityContract
from saed_v4_generative_path_stress_lab.budget import BudgetLedger
from saed_v4_generative_path_stress_lab.errors import BudgetError,ContractError

def test_budget_exhaustion(config):
    b=BudgetLedger(RolloutBudget.from_mapping(config['budget']));b.consume('generated_paths',config['budget']['max_generated_paths'])
    with pytest.raises(BudgetError):b.consume('generated_paths',1)
@pytest.mark.parametrize('key',['hidden_evaluation_queries','protected_evidence_exposure_limit'])
def test_protected_budget_must_be_zero(config,key):
    x=copy.deepcopy(config['budget']);x[key]=1
    with pytest.raises(ContractError):RolloutBudget.from_mapping(x)
def test_synthetic_positive_evidence_rejected(config):
    x=copy.deepcopy(config['exploitability']);x['synthetic_gain_is_positive_evidence']=True
    with pytest.raises(ContractError):ExploitabilityContract.from_mapping(x)
def test_nondeterministic_generator_rejected(config):
    x=copy.deepcopy(config['generator_program']);x['deterministic']=False
    with pytest.raises(ContractError):GeneratorProgramContract.from_mapping(x)
