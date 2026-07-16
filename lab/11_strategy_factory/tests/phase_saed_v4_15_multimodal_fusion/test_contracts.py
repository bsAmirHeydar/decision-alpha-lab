import pytest
from saed_v4_multimodal_fusion.contracts import FusionConfig,CandidateSpec,SupportPolicy,MissingnessPolicy,ComputeExposureBudget
from saed_v4_multimodal_fusion.errors import ContractError

def test_valid_contracts(load):
 FusionConfig.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_15/reference_fusion_config.json'))
 [CandidateSpec.from_mapping(x) for x in load('lab/11_strategy_factory/examples/saed_v4_15/reference_candidate_catalog.json')]
 SupportPolicy.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_15/reference_support_policy.json'));MissingnessPolicy.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_15/reference_missingness_policy.json'));ComputeExposureBudget.from_mapping(load('lab/11_strategy_factory/examples/saed_v4_15/reference_compute_exposure_budget.json'))
@pytest.mark.parametrize('field',['unknown','extra','future'])
def test_unknown_config_fields_fail(load,field):
 x=load('lab/11_strategy_factory/examples/saed_v4_15/reference_fusion_config.json');x[field]=1
 with pytest.raises(ContractError):FusionConfig.from_mapping(x)
@pytest.mark.parametrize('bad',[0,1,2,3])
def test_common_dim_floor(load,bad):
 x=load('lab/11_strategy_factory/examples/saed_v4_15/reference_fusion_config.json');x['common_dim']=bad
 with pytest.raises(ContractError):FusionConfig.from_mapping(x)
@pytest.mark.parametrize('algo',['oracle','remote_llm','order_router'])
def test_unknown_algorithm_fails(load,algo):
 x=load('lab/11_strategy_factory/examples/saed_v4_15/reference_candidate_catalog.json')[0];x['algorithm']=algo
 with pytest.raises(ContractError):CandidateSpec.from_mapping(x)
