from decimal import Decimal
from strategy_factory_economics_v3 import *
def test_cost_increases_are_non_improving_for_volume():
    q,s,a,g,r,b,m=fixture(); solver=MaximumLossSolver(); base=solver.solve(g,q,s,a,m,b); suite=EconomicStressSuite()
    for sc in (StressScenario('s1','1',StressKind.SPREAD_MULTIPLIER,Decimal('3')),StressScenario('s2','1',StressKind.COMMISSION_MULTIPLIER,Decimal('2')),StressScenario('s3','1',StressKind.SLIPPAGE_POINTS,Decimal('8')),StressScenario('s4','1',StressKind.GAP_POINTS,Decimal('20'))):
        r=suite.run_one(sc,base,q,s,m,g,a,b); assert r.passed_monotonicity
def test_minimum_commission_is_included():
    q,s,a,g,r,b,m=fixture(); e=MaximumLossSolver().solve(g,q,s,a,m,b); assert e.costs.commission_cash>0
