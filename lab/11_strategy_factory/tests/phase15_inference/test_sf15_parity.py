from strategy_factory_inference.examples import *
from strategy_factory_inference.parity import evaluate_parity
from strategy_factory_inference.enums import ParityVerdict

def test_parity_passes_exact_reference():
 v=make_vectors();r=evaluate_parity("manifest",v,[x.expected_raw_score for x in v],[x.expected_calibrated_score for x in v],[x.expected_class for x in v],raw_tolerance=1e-12,calibrated_tolerance=1e-12)
 assert r.verdict==ParityVerdict.PASS and r.failed_count==0

def test_parity_fails_score_or_class_difference():
 v=make_vectors();raw=[x.expected_raw_score for x in v];raw[0]+=1e-3
 r=evaluate_parity("manifest",v,raw,[x.expected_calibrated_score for x in v],[x.expected_class for x in v],raw_tolerance=1e-6)
 assert r.verdict==ParityVerdict.FAIL and r.failed_count==1
