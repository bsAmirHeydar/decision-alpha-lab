from decimal import Decimal
from strategy_factory_treatments_v3 import *
def test_no_trail_and_atr_trail_are_explicit():
 _,n=NoTrail().invoke(reference_context()); _,a=AtrTrail().invoke(reference_context(),{'atr_multiple':'2'})
 assert n.mode=='none' and a.distance==Decimal('1.0')
def test_fixed_target_can_coexist_with_trailing_atoms_as_independent_plans():
 c=reference_context(); _,target=FixedRTarget().invoke(c); _,trail=BreakEvenTrail().invoke(c)
 assert target.legs[0].target_price is not None and trail.mode=='break_even'
def test_management_partial_and_runner_style_are_composable_contracts():
 c=reference_context(); _,m=PartialExitAtR().invoke(c); _,r=RunnerTarget().invoke(c)
 assert m.rules[0].quantity_fraction==Decimal('0.5') and r.no_fixed_target
def test_equity_fraction_sizing_is_preliminary_cash_budget():
 _,p=EquityFractionRisk().invoke(reference_context(),{'fraction':'0.01'}); assert p.requested_value==Decimal('100.00') and p.cap_value==Decimal('250')
def test_confidence_scaling_monotonic():
 a=ConfidenceScaling(); c=reference_context(); _,p=a.invoke(c,{'floor_confidence':'0.5','ceiling_confidence':'0.9','base_cash':'100'}); assert p.requested_value==Decimal('62.5')
