import pytest
from saed_v4_causal_treatment_policy_value.authority import assert_operation,boundary_record,ALLOWED,FORBIDDEN
from saed_v4_causal_treatment_policy_value.errors import AuthorityError

@pytest.mark.parametrize('operation',sorted(ALLOWED))
def test_allowed_operations(operation):assert assert_operation(operation)

@pytest.mark.parametrize('operation',sorted(FORBIDDEN))
def test_forbidden_operations(operation):
 with pytest.raises(AuthorityError):assert_operation(operation)

def test_boundary_all_authorities_false():
 b=boundary_record();assert all(b[k] is False for k in ['real_causal_claim_authority','production_treatment_ranking_authority','decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority'])

def test_budget_passes(load,art):
 l=load(f'{art}/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON');assert l['passed'] and not any(l['exceeded'].values()) and l['usage']['protected_evidence_exposures']==0 and l['usage']['hidden_evaluation_queries']==0
