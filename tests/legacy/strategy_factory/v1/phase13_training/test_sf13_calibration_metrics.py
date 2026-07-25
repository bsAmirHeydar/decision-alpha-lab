from strategy_factory_training.calibration import *
from strategy_factory_training.metrics import *
from strategy_factory_training.enums import CalibrationMethod

def test_platt_calibration_is_deterministic():
    raw=[-2,-1,1,2];y=[0,0,1,1];a=fit_calibration(CalibrationMethod.PLATT,raw,y,"m",["a","b","c","d"]);b=fit_calibration(CalibrationMethod.PLATT,raw,y,"m",["a","b","c","d"])
    assert a.calibration_hash==b.calibration_hash and apply_calibration(2,a)>apply_calibration(-2,a)

def test_metrics_known_behavior():
    y=[0,0,1,1];good=[0.1,0.2,0.8,0.9];bad=[0.9,0.8,0.2,0.1]
    assert binary_log_loss(y,good)<binary_log_loss(y,bad) and roc_auc(y,good)==1.0
