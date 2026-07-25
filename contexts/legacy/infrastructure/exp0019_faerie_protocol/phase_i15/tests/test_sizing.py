from dataclasses import replace
from fp_i15_paper import *
def test_buy_risk_cap(buy_plan): assert buy_plan.sizing.estimated_max_loss<=buy_plan.sizing.risk_budget+1e-8
def test_sell_risk_cap(sell_plan): assert sell_plan.sizing.estimated_max_loss<=sell_plan.sizing.risk_budget+1e-8
def test_sell_uses_adjusted_distance(sell_plan,sell_spec):
 ticks=sell_plan.geometry.stop_distance/sell_spec.tick_size; assert abs(sell_plan.sizing.loss_per_lot-ticks*sell_spec.tick_value_loss_per_lot)<1e-9
def test_volume_floored_to_step(buy_plan,buy_spec): assert abs((buy_plan.sizing.volume/buy_spec.volume_step)-round(buy_plan.sizing.volume/buy_spec.volume_step))<1e-8
def test_min_volume_rejects(buy_plan,buy_spec,risk):
 s=replace(buy_spec,volume_min=10); r=size_fixed_risk(buy_plan.geometry,s,risk); assert r.status==GeometryStatus.BLOCKED
def test_commission_included(buy_plan,buy_spec,risk):
 r=size_fixed_risk(buy_plan.geometry,buy_spec,replace(risk,round_trip_cost_per_lot=5)); assert r.loss_per_lot>buy_plan.sizing.loss_per_lot
