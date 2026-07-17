import copy,pytest
from saed_v4_portfolio_execution_economics import run_reference
from saed_v4_portfolio_execution_economics.errors import SAEDV437Error

MUTATIONS=[
 ("upstream_unknown",lambda f:f["upstream"][0].__setitem__("unknown",1)),
 ("upstream_authority",lambda f:f["upstream"][0].__setitem__("production_authorized",True)),
 ("constitution_order",lambda f:f["constitution"].__setitem__("automatic_order_submission_allowed",True)),
 ("constitution_capital",lambda f:f["constitution"].__setitem__("capital_activation_allowed",True)),
 ("future_instrument",lambda f:f["instruments"][0].__setitem__("known_time","2099-01-01T00:00:00Z")),
 ("duplicate_instrument",lambda f:f["instruments"][1].__setitem__("instrument_id",f["instruments"][0]["instrument_id"])),
 ("bad_lot",lambda f:f["instruments"][0].__setitem__("min_lot",3000000)),
 ("future_fx",lambda f:f["fx_rates"][0].__setitem__("known_time","2099-01-01T00:00:00Z")),
 ("negative_fx",lambda f:f["fx_rates"][0].__setitem__("mid",-1)),
 ("future_cost",lambda f:f["cost_schedules"][0].__setitem__("known_time","2099-01-01T00:00:00Z")),
 ("negative_cost",lambda f:f["cost_schedules"][0].__setitem__("commission_value",-1)),
 ("bad_curve",lambda f:f["liquidity_profiles"][0].__setitem__("volume_curve",[.2,.2,.2,.2])),
 ("participation_high",lambda f:f["liquidity_profiles"][0].__setitem__("max_participation_rate",.4)),
 ("future_liq",lambda f:f["liquidity_profiles"][0].__setitem__("known_time","2099-01-01T00:00:00Z")),
 ("asymmetric_corr",lambda f:f["dependence"]["correlation_matrix"][0].__setitem__(1,.9)),
 ("diag_corr",lambda f:f["dependence"]["correlation_matrix"][0].__setitem__(0,.9)),
 ("missing_vol",lambda f:f["dependence"]["volatility_vector"].pop("SYN_EQ_A")),
 ("bad_cash",lambda f:f["constraints"].__setitem__("cash_reserve",11000000)),
 ("high_participation",lambda f:f["constraints"].__setitem__("max_participation_rate",.5)),
 ("future_constraints",lambda f:f["constraints"].__setitem__("known_time","2099-01-01T00:00:00Z")),
 ("future_opp",lambda f:f["opportunities"][0].__setitem__("known_time","2099-01-01T00:00:00Z")),
 ("bad_direction",lambda f:f["opportunities"][0].__setitem__("direction","SIDEWAYS")),
 ("overmax_opp",lambda f:f["opportunities"][0].__setitem__("requested_notional",9999999)),
 ("duplicate_opp",lambda f:f["opportunities"][1].__setitem__("opportunity_id",f["opportunities"][0]["opportunity_id"])),
 ("review_hash",lambda f:f["reviews"][0].__setitem__("plan_hash","0"*64)),
 ("review_role",lambda f:f["reviews"][0].__setitem__("role","TRADER")),
 ("duplicate_review",lambda f:f["reviews"][1].__setitem__("review_id",f["reviews"][0]["review_id"])),
 ("fill_unknown",lambda f:f["synthetic_fills"][0].__setitem__("opportunity_id","UNKNOWN")),
 ("fill_negative",lambda f:f["synthetic_fills"][0].__setitem__("filled_units",-1)),
 ("stress_negative",lambda f:f["stress_scenarios"][0].__setitem__("cost_multiplier",-1)),
]
@pytest.mark.parametrize("name,mutator",MUTATIONS,ids=[x[0] for x in MUTATIONS])
def test_mutation_fails_closed(fixture,name,mutator):
 f=copy.deepcopy(fixture); mutator(f)
 with pytest.raises((SAEDV437Error,ValueError,KeyError,ZeroDivisionError)): run_reference(f)
