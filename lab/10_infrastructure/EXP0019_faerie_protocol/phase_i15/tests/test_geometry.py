from dataclasses import replace
from fp_i15_paper import *
def test_buy_stop_unchanged(buy_winner,buy_quote,buy_spec,risk):
 g=build_geometry(buy_winner,buy_quote,buy_spec,risk); assert g.adjusted_stop==buy_winner.raw_structural_stop
def test_sell_adds_exact_spread(sell_winner,sell_quote,sell_spec,risk):
 g=build_geometry(sell_winner,sell_quote,sell_spec,risk); assert abs(g.adjusted_stop-(sell_winner.raw_structural_stop+sell_quote.spread))<1e-12
def test_buy_entry_ask(buy_winner,buy_quote,buy_spec,risk): assert build_geometry(buy_winner,buy_quote,buy_spec,risk).planned_entry==buy_quote.ask
def test_sell_entry_bid(sell_winner,sell_quote,sell_spec,risk): assert build_geometry(sell_winner,sell_quote,sell_spec,risk).planned_entry==sell_quote.bid
def test_worst_case_buy_adds_slippage(buy_winner,buy_quote,buy_spec,risk):
 g=build_geometry(buy_winner,buy_quote,buy_spec,risk); assert g.worst_case_entry==g.planned_entry+risk.max_slippage_price
def test_worst_case_sell_subtracts_slippage(sell_winner,sell_quote,sell_spec,risk):
 g=build_geometry(sell_winner,sell_quote,sell_spec,risk); assert g.worst_case_entry==g.planned_entry-risk.max_slippage_price
def test_buy_target_positive(buy_winner,buy_quote,buy_spec,risk):
 g=build_geometry(buy_winner,buy_quote,buy_spec,risk); assert g.target>g.planned_entry
def test_sell_target_negative(sell_winner,sell_quote,sell_spec,risk):
 g=build_geometry(sell_winner,sell_quote,sell_spec,risk); assert g.target<g.planned_entry
def test_invalid_buy_stop_blocks(buy_winner,buy_quote,buy_spec,risk): assert build_geometry(replace(buy_winner,raw_structural_stop=101),buy_quote,buy_spec,risk).status==GeometryStatus.BLOCKED
def test_invalid_sell_stop_blocks(sell_winner,sell_quote,sell_spec,risk): assert build_geometry(replace(sell_winner,raw_structural_stop=199),sell_quote,sell_spec,risk).status==GeometryStatus.BLOCKED
def test_wrong_trade_symbol_blocks(buy_winner,sell_quote,buy_spec,risk): assert 'FP_PAPER_TRADE_SYMBOL_NOT_PROTECTED' in build_geometry(buy_winner,sell_quote,buy_spec,risk).reason_codes
