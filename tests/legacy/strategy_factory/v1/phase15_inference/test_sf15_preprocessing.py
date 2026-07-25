import math,pytest
from strategy_factory_inference.examples import PREPROCESSING
from strategy_factory_inference.preprocessing import transform

def test_preprocessing_exact_values():
 out=transform((0.9,0.4,1.5,0.8),(False,False,False,False),PREPROCESSING)
 assert out==pytest.approx((2/3,0.75,0.6,1.2),abs=1e-15)

def test_missing_uses_train_impute():
 out=transform((999,999,999,999),(True,True,True,True),PREPROCESSING)
 assert out==pytest.approx((-1/12,0.25,-0.15,0.0),abs=1e-15)

def test_observed_nonfinite_fails():
 with pytest.raises(ValueError):transform((math.nan,0,0,0),(False,False,False,False),PREPROCESSING)
