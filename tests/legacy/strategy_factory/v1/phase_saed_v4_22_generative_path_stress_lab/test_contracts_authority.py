import copy,pytest
from saed_v4_generative_path_stress_lab.contracts import *
from saed_v4_generative_path_stress_lab.errors import ContractError,AuthorityError
from saed_v4_generative_path_stress_lab.authority import authority_boundary,assert_no_authority

@pytest.mark.parametrize('key,cls',[('upstream_intake',UpstreamIntakeContract),('state_schema',StateSchemaContract),('generator_program',GeneratorProgramContract),('path_invariants',PathInvariantContract),('stress_program',StressProgramContract),('fidelity',FidelityContract),('exploitability',ExploitabilityContract),('budget',RolloutBudget)])
def test_valid_contracts(config,key,cls): assert cls.from_mapping(config[key])
@pytest.mark.parametrize('key,cls',[('upstream_intake',UpstreamIntakeContract),('state_schema',StateSchemaContract),('generator_program',GeneratorProgramContract),('path_invariants',PathInvariantContract),('stress_program',StressProgramContract),('fidelity',FidelityContract),('exploitability',ExploitabilityContract),('budget',RolloutBudget)])
def test_unknown_field_rejected(config,key,cls):
    x=copy.deepcopy(config[key]);x['unknown']=1
    with pytest.raises(ContractError):cls.from_mapping(x)
@pytest.mark.parametrize('field',['decision','execution','promotion','production','risk_allocation','runtime','order_submission','positive_alpha_evidence'])
def test_authority_denied(field): assert authority_boundary()['authority'][field] is False
def test_authority_escalation_rejected():
    with pytest.raises(AuthorityError):assert_no_authority({'authority':{'runtime':True}})
