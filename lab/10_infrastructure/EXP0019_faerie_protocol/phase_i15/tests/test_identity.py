from dataclasses import replace
from fp_i15_paper import *
def test_spread_changes_geometry_id(sell_winner,sell_quote,sell_spec,risk): assert build_geometry(sell_winner,sell_quote,sell_spec,risk).geometry_id!=build_geometry(sell_winner,replace(sell_quote,quote_id='Q2',ask=200.25),sell_spec,risk).geometry_id
def test_slippage_changes_sizing(buy_winner,buy_quote,buy_spec,risk):
 a=build_geometry(buy_winner,buy_quote,buy_spec,risk);b=build_geometry(buy_winner,buy_quote,buy_spec,replace(risk,max_slippage_price=.5));assert size_fixed_risk(a,buy_spec,risk).sizing_id!=size_fixed_risk(b,buy_spec,replace(risk,max_slippage_price=.5)).sizing_id
def test_policy_hashes_unique(): assert len({paper_policy(p).policy_hash for p in PaperPolicyProfile})==len(PaperPolicyProfile)
def test_plan_hash_length(buy_plan): assert len(buy_plan.plan_hash)==64
