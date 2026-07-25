import pytest
from strategy_factory_inference.examples import *
from strategy_factory_inference.preprocessing import transform
from strategy_factory_inference.reference import *

def test_reference_prediction():
 z=transform((0.9,0.4,1.5,0.8),(False,False,False,False),PREPROCESSING)
 raw=linear_score(z,WEIGHTS,BIAS);prob=calibrate(raw,CALIBRATION)
 assert raw==pytest.approx(1.445,abs=1e-15)
 assert prob==pytest.approx(0.809227736160,abs=1e-12)
 assert classify(prob,CALIBRATION.threshold)==1

def test_all_parity_vectors_self_consistent():
 for v in make_vectors():
  z=transform(v.values,v.missing,PREPROCESSING); raw=linear_score(z,WEIGHTS,BIAS); p=calibrate(raw,CALIBRATION)
  assert z==pytest.approx(v.expected_transformed,abs=1e-15)
  assert raw==pytest.approx(v.expected_raw_score,abs=1e-15)
  assert p==pytest.approx(v.expected_calibrated_score,abs=1e-15)
