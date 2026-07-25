from decimal import Decimal
from strategy_factory_treatments_v3 import *
def test_fixed_distance_stop_side_and_spread():
 _,l=FixedDistanceStop().invoke(reference_context(TradeSide.LONG),{'distance_points':'20'}); _,s=FixedDistanceStop().invoke(reference_context(TradeSide.SHORT),{'distance_points':'20'})
 assert l.stop_price==Decimal('99.82'); assert s.stop_price==Decimal('100.20')
def test_wider_stop_monotonically_increases_distance():
 a=FixedDistanceStop(); _,x=a.invoke(reference_context(),{'distance_points':'20'}); _,y=a.invoke(reference_context(),{'distance_points':'200'}); assert y.distance>x.distance
def test_fixed_r_uses_executable_entry_price():
 _,l=FixedRTarget().invoke(reference_context(),{'risk_points':'100','reward_multiple':'2'}); _,s=FixedRTarget().invoke(reference_context(TradeSide.SHORT),{'risk_points':'100','reward_multiple':'2'})
 assert l.legs[0].target_price==Decimal('102.02'); assert s.legs[0].target_price==Decimal('98.00')
def test_runner_has_no_fixed_target():
 _,p=RunnerTarget().invoke(reference_context()); assert p.no_fixed_target and p.legs[0].is_runner and p.legs[0].target_price is None
def test_multi_target_allocations_sum_to_one():
 _,p=MultiTargetLadder().invoke(reference_context(),{'leg_count':4}); assert sum(x.quantity_fraction for x in p.legs)==Decimal('1')
