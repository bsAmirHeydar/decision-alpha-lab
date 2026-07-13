import numpy as np, pytest
from strategy_factory_promotion_v3.nulls import *
from strategy_factory_promotion_v3.enums import NullKind,EvidenceStatus
from strategy_factory_promotion_v3.golden import golden_returns,golden_baseline
from strategy_factory_promotion_v3.errors import PromotionError

def test_random_direction_is_seeded(): assert np.array_equal(random_direction([1,2,3],seed=9),random_direction([1,2,3],seed=9))
def test_label_permutation_preserves_values(): assert sorted(label_permutation([1,2,3,4],seed=2))==[1,2,3,4]
def test_delayed_trigger_pads_past_only(): assert np.array_equal(delayed_trigger([1,2,3,4],2),[0,0,1,2])
def test_matched_control_does_not_cross_groups():
    out=matched_control([1,2,10,20],['a','a','b','b'],seed=1); assert set(out[:2])=={1,2} and set(out[2:])=={10,20}
def test_strong_observed_passes_manual_baseline():
    r=evaluate_null(NullKind.MANUAL_BASELINE,golden_returns(80),golden_baseline(80),iterations=500); assert r.status is EvidenceStatus.PASS
def test_mandatory_coverage_detects_missing():
    r=evaluate_null(NullKind.MANUAL_BASELINE,golden_returns(50),golden_baseline(50),iterations=200); assert not mandatory_null_coverage([r],[NullKind.MANUAL_BASELINE,NullKind.MATCHED_TIME])['passed']
def test_null_length_mismatch_rejected():
    with pytest.raises(PromotionError): evaluate_null(NullKind.MATCHED_TIME,[1,2],[1],iterations=200)
