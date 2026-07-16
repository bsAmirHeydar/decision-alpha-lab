import pytest
from saed_v4_distributional_survival_tail.contracts import EventDefinitionRegistry,CensoringPolicy,DatasetSpec,ModelConfig,CandidateSpec,TailPolicy,ComputeExposureBudget
from saed_v4_distributional_survival_tail.errors import ContractError

def test_valid_contracts(load):
 EventDefinitionRegistry.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_16/reference_event_definition_registry.json'));CensoringPolicy.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_16/reference_censoring_policy.json'));DatasetSpec.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_16/reference_dataset_spec.json'));ModelConfig.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_16/reference_model_config.json'));[CandidateSpec.from_mapping(x) for x in load('lab/11_strategy_factory/examples/saed_v4_16/reference_candidate_catalog.json')];TailPolicy.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_16/reference_tail_policy.json'));ComputeExposureBudget.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_16/reference_compute_exposure_budget.json'))
@pytest.mark.parametrize('name',['unknown','future','extra'])
def test_unknown_event_registry_fields_fail(load,name):
 x=load('lab/11_strategy_factory/examples/saed_v4_16/reference_event_definition_registry.json');x[name]=1
 with pytest.raises(ContractError):EventDefinitionRegistry.from_mapping(x)
def test_unknown_cause_fails(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_16/reference_event_definition_registry.json');x['causes'][0]='oracle_event'
 with pytest.raises(ContractError):EventDefinitionRegistry.from_mapping(x)
def test_censored_as_outcome_safeguard_required(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_16/reference_censoring_policy.json');x['censored_is_never_outcome']=False
 with pytest.raises(ContractError):CensoringPolicy.from_mapping(x)
def test_chronological_split_required(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_16/reference_dataset_spec.json');x['chronological_split']=False
 with pytest.raises(ContractError):DatasetSpec.from_mapping(x)
def test_monotone_quantiles_required(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_16/reference_model_config.json');x['monotone_quantiles']=False
 with pytest.raises(ContractError):ModelConfig.from_mapping(x)
def test_protected_exposure_budget_zero(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_16/reference_compute_exposure_budget.json');x['protected_evidence_exposure_limit']=1
 with pytest.raises(ContractError):ComputeExposureBudget.from_mapping(x)
