import pytest
from saed_v4_causal_mechanism_discovery.contracts import VariableRegistry,EnvironmentRegistry,GraphConstraints,DiscoveryConfig,CandidateSpec,ComputeExposureBudget
from saed_v4_causal_mechanism_discovery.errors import ContractError

def test_valid_contracts(load):
 VariableRegistry.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_17/reference_variable_registry.json'));EnvironmentRegistry.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_17/reference_environment_registry.json'));GraphConstraints.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_17/reference_graph_constraints.json'));DiscoveryConfig.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_17/reference_discovery_config.json'));[CandidateSpec.from_mapping(x) for x in load('lab/11_strategy_factory/examples/saed_v4_17/reference_candidate_catalog.json')];ComputeExposureBudget.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_17/reference_compute_exposure_budget.json'))
@pytest.mark.parametrize('field',['unknown','oracle','future'])
def test_variable_registry_unknown_field_rejected(load,field):
 x=load('lab/11_strategy_factory/examples/saed_v4_17/reference_variable_registry.json');x[field]=1
 with pytest.raises(ContractError):VariableRegistry.from_mapping(x)
def test_latent_claim_rejected(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_17/reference_variable_registry.json');x['latent_variables_claimable']=True
 with pytest.raises(ContractError):VariableRegistry.from_mapping(x)
def test_transport_claim_rejected(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_17/reference_environment_registry.json');x['transport_claims_allowed']=True
 with pytest.raises(ContractError):EnvironmentRegistry.from_mapping(x)
def test_causal_claim_ceiling_rejected(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_17/reference_discovery_config.json');x['claim_ceiling']='causal_confirmed'
 with pytest.raises(ContractError):DiscoveryConfig.from_mapping(x)
def test_protected_exposure_must_be_zero(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_17/reference_compute_exposure_budget.json');x['protected_evidence_exposure_limit']=1
 with pytest.raises(ContractError):ComputeExposureBudget.from_mapping(x)
def test_hidden_queries_must_be_zero(load):
 x=load('lab/11_strategy_factory/examples/saed_v4_17/reference_compute_exposure_budget.json');x['hidden_evaluation_query_limit']=1
 with pytest.raises(ContractError):ComputeExposureBudget.from_mapping(x)
