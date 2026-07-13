import numpy as np, pytest
from strategy_factory_promotion_v3.winner_overfit import *
from strategy_factory_promotion_v3.errors import PromotionError

def matrix():
    rng=np.random.default_rng(7); x=rng.normal(0,.05,(8,4)); x[:,0]+=.2; return x

def test_deflation_uses_total_choice_count(): assert deflated_performance(2.0,sample_count=200,total_choice_count=100)['benchmark']>deflated_performance(2.0,sample_count=200,total_choice_count=2)['benchmark']
def test_pbo_is_deterministic(): assert pbo_cscv(matrix(),seed=4)==pbo_cscv(matrix(),seed=4)
def test_pbo_range(): assert 0<=pbo_cscv(matrix())['pbo']<=1
def test_odd_cscv_blocks_rejected():
    with pytest.raises(PromotionError,match='odd_cscv_blocks'): pbo_cscv(np.ones((5,2)))
def test_white_reality_check_range(): assert 0<=white_reality_check(matrix(),iterations=200,block_size=2)['p_value']<=1
def test_spa_range(): assert 0<=spa_test(matrix(),iterations=200,block_size=2)['p_value']<=1
def test_reality_check_deterministic(): assert white_reality_check(matrix(),iterations=200,seed=5)==white_reality_check(matrix(),iterations=200,seed=5)
