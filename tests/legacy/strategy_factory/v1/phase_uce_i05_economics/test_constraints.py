from decimal import Decimal
from dataclasses import replace
from strategy_factory_economics_v3 import *
def test_volume_is_floored_not_rounded_up():
    q,s,a,g,r,b,m=fixture(); out=BrokerConstraintSolver().solve(s,q,g,Decimal('1.1001'),Decimal('1.0981'),Decimal('1.1041'),Decimal('0.019'),a.free_margin); assert out.volume==Decimal('0.01')
def test_minimum_stop_is_widened_conservatively():
    q,s,a,g,r,b,m=fixture(); g=replace(g,logical_stop_price=Decimal('1.10005')); out=BrokerConstraintSolver().solve(s,q,g,Decimal('1.1001'),Decimal('1.10005'),Decimal('1.1041'),Decimal('0.1'),a.free_margin); assert abs(out.entry_price-out.stop_price)>=s.stops_level_points*s.point
def test_disabled_symbol_rejects():
    q,s,a,g,r,b,m=fixture(); s=replace(s,trade_status=TradeStatus.DISABLED); out=BrokerConstraintSolver().solve(s,q,g,g.logical_entry_price,g.logical_stop_price,g.logical_target_price,Decimal('1'),a.free_margin); assert not out.accepted
