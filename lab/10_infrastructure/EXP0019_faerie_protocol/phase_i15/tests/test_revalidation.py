from dataclasses import replace
from fp_i15_paper import *
def test_same_quote_unchanged(buy_plan,proof,buy_winner,readiness,buy_quote,buy_spec,risk): assert revalidate_plan(buy_plan,proof,buy_winner,readiness,buy_quote,buy_spec,risk,buy_plan.created_utc_ms).disposition==RevalidationDisposition.UNCHANGED
def test_new_quote_reprices(buy_plan,proof,buy_winner,readiness,buy_quote,buy_spec,risk): assert revalidate_plan(buy_plan,proof,buy_winner,readiness,replace(buy_quote,quote_id='Q2',ask=100.5),buy_spec,risk,buy_plan.created_utc_ms+1).disposition==RevalidationDisposition.REPRICED
def test_sell_wider_spread_changes_stop(sell_plan,proof,sell_winner,readiness,sell_quote,sell_spec,risk):
 n=replace(sell_quote,quote_id='Q2',ask=200.5);r=revalidate_plan(sell_plan,proof,sell_winner,readiness,n,sell_spec,risk,sell_plan.created_utc_ms+1);assert r.plan.geometry.adjusted_stop>sell_plan.geometry.adjusted_stop
def test_invalid_revalidation_blocks(buy_plan,proof,buy_winner,readiness,buy_quote,buy_spec,risk):
 q=replace(buy_quote,quote_id='Q2',ask=98.5,bid=98.25); assert revalidate_plan(buy_plan,proof,buy_winner,readiness,q,buy_spec,risk,buy_plan.created_utc_ms+1).disposition==RevalidationDisposition.BLOCKED
