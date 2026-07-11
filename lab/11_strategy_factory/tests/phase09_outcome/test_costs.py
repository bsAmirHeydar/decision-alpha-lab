import pytest
from strategy_factory_outcome import *
def test_cost_reconciliation():
    r=CostRegistry();m=FixedCostModel("m","1",False,entry_spread=1,exit_spread=1,entry_slippage=0.5,exit_slippage=0.5,commission_r=.1);r.register(m);r.compile();c=r.resolve("m","1").compute(CostRequest("c",10));assert c.total_cost_points==3;assert abs(c.total_cost_r-.4)<1e-12
def test_duplicate_cost_model_rejected():
    r=CostRegistry();m=FixedCostModel();r.register(m)
    with pytest.raises(ValueError):r.register(m)
def test_registry_hash_stable():
    a=CostRegistry();a.register(FixedCostModel());a.compile();b=CostRegistry();b.register(FixedCostModel());b.compile();assert a.registry_hash==b.registry_hash
