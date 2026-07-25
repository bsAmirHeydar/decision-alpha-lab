import pytest
from strategy_factory_statistics.confidence import wilson_interval,normal_mean_interval

def test_wilson_bounds():
    x=wilson_interval('win_rate','all',8,10)
    assert 0<=x.lower<x.estimate<x.upper<=1
def test_normal_zero_variance():
    x=normal_mean_interval('mean','all',1,0,10)
    assert x.lower==x.upper==1
def test_invalid_counts():
    with pytest.raises(ValueError): wilson_interval('x','all',2,1)
def test_interval_hash_deterministic():
    assert wilson_interval('x','g',5,10).interval_hash==wilson_interval('x','g',5,10).interval_hash
