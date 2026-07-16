import copy,pytest
from saed_v4_foundation_model_adapters.validation import validate_config,validate_intakes,validate_candidates,validate_disclosures,validate_domain_shift_policy,validate_budget
from saed_v4_foundation_model_adapters.errors import ContractError

def test_valid_contracts(inputs):
 c=validate_config(inputs['adapter_config_doc']);i=validate_intakes(inputs['intake_docs']);assert len(validate_candidates(inputs['candidate_docs'],i))==6;assert len(validate_disclosures(inputs['disclosure_docs'],i))==6;validate_domain_shift_policy(inputs['domain_policy_doc']);validate_budget(inputs['budget_doc'])
@pytest.mark.parametrize('field',['known_time_only','frozen_upstream','local_execution_only'])
def test_mandatory_safety_flags(inputs,field):
 x=copy.deepcopy(inputs['adapter_config_doc']);x[field]=False
 with pytest.raises(ContractError):validate_config(x)
def test_unknown_field_rejected(inputs):
 x=copy.deepcopy(inputs['adapter_config_doc']);x['extra']=1
 with pytest.raises(ContractError):validate_config(x)
def test_unknown_family_rejected(inputs):
 xs=copy.deepcopy(inputs['intake_docs']);xs[0]['family']='oracle_v99'
 with pytest.raises(ContractError):validate_intakes(xs)
def test_remote_inference_rejected(inputs):
 xs=copy.deepcopy(inputs['intake_docs']);xs[0]['remote_inference_forbidden']=False
 with pytest.raises(ContractError):validate_intakes(xs)
def test_duplicate_candidate_rejected(inputs):
 ints=validate_intakes(inputs['intake_docs']);xs=copy.deepcopy(inputs['candidate_docs']);xs[1]['candidate_id']=xs[0]['candidate_id']
 with pytest.raises(ContractError):validate_candidates(xs,ints)
