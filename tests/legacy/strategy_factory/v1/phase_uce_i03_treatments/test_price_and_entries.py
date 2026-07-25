from decimal import Decimal
import pytest
from strategy_factory_treatments_v3 import *
def test_market_entry_uses_ask_for_long_and_bid_for_short():
 a=ImmediateMarketEntry(); _,lp=a.invoke(reference_context(TradeSide.LONG)); _,sp=a.invoke(reference_context(TradeSide.SHORT))
 assert lp.legs[0].trigger_price==Decimal('100.02'); assert sp.legs[0].trigger_price==Decimal('100.00')
def test_passive_limits_are_on_correct_executable_side():
 a=PassiveLimitEntry(); _,lp=a.invoke(reference_context(TradeSide.LONG),{'offset_points':'10'}); _,sp=a.invoke(reference_context(TradeSide.SHORT),{'offset_points':'10'})
 assert lp.legs[0].trigger_price==Decimal('99.92'); assert sp.legs[0].trigger_price==Decimal('100.10')
def test_breakout_stops_are_side_aware():
 a=BreakoutStopEntry(); _,lp=a.invoke(reference_context(TradeSide.LONG),{'buffer_points':'2'}); _,sp=a.invoke(reference_context(TradeSide.SHORT),{'buffer_points':'2'})
 assert lp.legs[0].trigger_price==Decimal('101.02'); assert sp.legs[0].trigger_price==Decimal('98.98')
def test_ladder_allocations_sum_to_one():
 _,p=LadderEntry().invoke(reference_context(),{'leg_count':4}); assert sum(x.allocation_fraction for x in p.legs)==Decimal('1')
def test_invalid_parameter_rejected():
 with pytest.raises(ParameterError): FixedDistanceStop().invoke(reference_context(),{'distance_points':'0'})
