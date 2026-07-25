import pytest
from saed_v4_distributional_survival_tail.authority import assert_operation,ALLOWED,FORBIDDEN
from saed_v4_distributional_survival_tail.errors import AuthorityError
@pytest.mark.parametrize('op',sorted(ALLOWED))
def test_allowed(op):assert assert_operation(op)
@pytest.mark.parametrize('op',sorted(FORBIDDEN))
def test_forbidden(op):
 with pytest.raises(AuthorityError):assert_operation(op)
def test_budget_pass(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON')['passed']
def test_zero_protected_exposure(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON');assert x['actual']['protected_evidence_exposures']==0==x['limits']['protected_evidence_exposures']
