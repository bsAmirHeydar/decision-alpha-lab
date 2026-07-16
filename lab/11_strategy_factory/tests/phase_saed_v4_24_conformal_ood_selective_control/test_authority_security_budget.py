import pytest
from saed_v4_conformal_ood_selective_control.authority import boundary
from saed_v4_conformal_ood_selective_control.budget import ResearchLedger
from saed_v4_conformal_ood_selective_control.contracts import ResearchBudget
from saed_v4_conformal_ood_selective_control.errors import AuthorityError, BudgetError
from saed_v4_conformal_ood_selective_control.security import scan
@pytest.mark.parametrize('key', ['promotion_authority','production_authorization','runtime_executable','risk_allocation_authority','execution_authority','order_submission','activate_runtime','online_learning','mutate_policy','send_order'])
def test_authority_flags_rejected(key):
    with pytest.raises(AuthorityError): scan({key: True})
def test_boundary_zero(): assert not any(boundary()['authority'].values())
@pytest.mark.parametrize('key', ['hidden_evaluation_queries','protected_evidence_exposures','runtime_compilations','order_submissions'])
def test_zero_budget_cannot_be_consumed(config, key):
    ledger = ResearchLedger(ResearchBudget.from_mapping(config['research_budget']))
    with pytest.raises(BudgetError): ledger.consume(key, 1)
