import numpy as np, pytest
from strategy_factory_promotion_v3.calibration import *
from strategy_factory_promotion_v3.golden import golden_probabilities,golden_labels,golden_returns
from strategy_factory_promotion_v3.errors import PromotionError

def test_brier_is_low_for_golden_predictions(): assert brier_score(golden_labels(),golden_probabilities())<.1
def test_log_loss_is_finite(): assert np.isfinite(log_loss(golden_labels(),golden_probabilities()))
def test_reliability_bins_preserve_count(): assert sum(r['count'] for r in reliability_bins(golden_labels(),golden_probabilities(),bins=8))==120
def test_ece_range(): assert 0<=expected_calibration_error(golden_labels(),golden_probabilities())<=1
def test_conformal_coverage_exact(): assert conformal_coverage([0,0],[1,1],[.2,1.2])==.5
def test_decision_curve_returns_thresholds(): assert len(decision_curve(golden_labels(30),golden_probabilities(30),(.25,.5,.75)))==3
def test_abstention_metrics_are_consistent():
    x=abstention_metrics(golden_labels(30),golden_probabilities(30)); assert abs(x['coverage']+x['abstention_rate']-1)<1e-12
def test_risk_tier_calibration_has_all_tiers(): assert set(risk_tier_calibration(golden_labels(12),golden_probabilities(12),['a']*6+['b']*6)['tiers'])=={'a','b'}
def test_build_calibration_report_has_identity():
    n=60; r=build_calibration_report(golden_labels(n),golden_probabilities(n),conformal_lower=[0]*n,conformal_upper=[1]*n,conformal_observed=golden_labels(n),target_coverage=.95,outcomes=golden_returns(n),risk_tiers=['low' if i%2 else 'high' for i in range(n)]); assert len(r.evidence_hash)==64
def test_invalid_probability_rejected():
    with pytest.raises(PromotionError): brier_score([0,1],[.2,1.2])
