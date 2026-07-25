import numpy as np, pytest
from strategy_factory_promotion_v3.stress import *
from strategy_factory_promotion_v3.enums import StressKind,EvidenceStatus
from strategy_factory_promotion_v3.golden import golden_returns
from strategy_factory_promotion_v3.errors import PromotionError

def test_cost_stress_is_incremental(): assert np.allclose(cost_stress([1,1],.1,2),[.9,.9])
def test_fill_stress_is_seeded(): assert np.array_equal(fill_stress([1]*20,.5,seed=3),fill_stress([1]*20,.5,seed=3))
def test_best_trade_removal_removes_largest(): assert np.array_equal(best_trade_removal([1,2,3,4],.25),[1,2,3,0])
def test_latency_stress_applies_adverse_move(): assert np.allclose(latency_stress([1,1],.01,10),[.9,.9])
def test_stress_result_passes_retention():
    r=evaluate_stress(StressKind.COST,golden_returns(30),cost_stress(golden_returns(30),.005,2),minimum_retention=.5); assert r.status is EvidenceStatus.PASS
def test_parameter_neighborhood_requires_plateau(): assert parameter_neighborhood({'left':.8,'center':1.0,'right':.85},center_key='center',minimum_retention=.7)['passed']
def test_aggregate_stress_fails_if_one_fails():
    a=evaluate_stress(StressKind.COST,[1,1],[.9,.9]); b=evaluate_stress(StressKind.FILL,[1,1],[-1,-1]); assert not aggregate_stress([a,b])['passed']
def test_invalid_drop_fraction_rejected():
    with pytest.raises(PromotionError): trade_drop_stress([1,2],1.0)
