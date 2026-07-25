from dataclasses import replace
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.model import validate_model_output,argmax_stable
from strategy_factory_policy_v3.enums import FallbackReason,CalibrationState

def ok(a=None,o=None,m=None,**kw): return validate_model_output(a or golden_admission(),o or golden_occurrence(),m or golden_output(),**kw)
def test_valid_model_passes(): assert ok()[0]
def test_stale_model_falls_back(): assert ok(o=replace(golden_occurrence(),known_time_ms=6001,feature_time_ms=6001))[1] is FallbackReason.STALE_MODEL
def test_missing_view_falls_back(): assert ok(o=replace(golden_occurrence(),views_present=('tabular',)))[1] is FallbackReason.MISSING_VIEW
def test_ood_falls_back(): assert ok(m=replace(golden_output(),novelty=.9))[1] is FallbackReason.OUT_OF_DISTRIBUTION
def test_low_confidence_falls_back(): assert ok(m=replace(golden_output(),uncertainty=.9))[1] is FallbackReason.LOW_CONFIDENCE
def test_degraded_calibration_requires_explicit_allow(): assert not ok(m=replace(golden_output(),calibration_state=CalibrationState.DEGRADED))[0] and ok(m=replace(golden_output(),calibration_state=CalibrationState.DEGRADED),allow_degraded_calibration=True)[0]
def test_action_support_violation_detected():
    a=replace(golden_admission(),actions=('enter_long',)); m=replace(golden_output(),action_probabilities={'enter_long':.8,'other':.2}); assert ok(a=a,m=m)[1] is FallbackReason.UNSUPPORTED_ACTION
def test_stable_argmax_uses_key_tiebreak(): assert argmax_stable({'b':.5,'a':.5})=='a'
