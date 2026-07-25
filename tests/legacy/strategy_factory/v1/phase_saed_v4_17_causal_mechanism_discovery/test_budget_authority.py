import pytest
from saed_v4_causal_mechanism_discovery.authority import assert_operation,FORBIDDEN
from saed_v4_causal_mechanism_discovery.errors import AuthorityError
@pytest.mark.parametrize('op',['read_frozen_v4_16_evidence','build_synthetic_causal_benchmark','audit_invariance','run_negative_controls','build_v4_18_handoff'])
def test_allowed(op):assert assert_operation(op)
@pytest.mark.parametrize('op',sorted(FORBIDDEN))
def test_forbidden(op):
 with pytest.raises(AuthorityError):assert_operation(op)
def test_budget_passed(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON')['passed']
def test_zero_protected_and_hidden(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON')['usage'];assert x['protected_evidence_exposures']==0 and x['hidden_evaluation_queries']==0
