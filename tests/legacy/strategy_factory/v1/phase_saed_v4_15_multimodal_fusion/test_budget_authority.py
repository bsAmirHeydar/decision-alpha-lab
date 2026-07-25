import pytest
from saed_v4_multimodal_fusion.authority import assert_operation,ALLOWED,FORBIDDEN
from saed_v4_multimodal_fusion.errors import AuthorityError
@pytest.mark.parametrize('op',sorted(ALLOWED))
def test_allowed(op):assert assert_operation(op)
@pytest.mark.parametrize('op',sorted(FORBIDDEN))
def test_forbidden(op):
 with pytest.raises(AuthorityError):assert_operation(op)
def test_budget_pass(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON')['passed']
def test_zero_protected_exposure(load):
 l=load('releases/history/strategy_factory/artifacts/saed_v4_15/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON');assert l['protected_evidence_exposures']==0 and l['outcome_label_exposures']==0
