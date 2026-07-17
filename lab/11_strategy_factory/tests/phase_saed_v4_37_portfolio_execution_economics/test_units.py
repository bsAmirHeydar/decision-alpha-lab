import copy,pytest
from saed_v4_portfolio_execution_economics.fx import freeze_fx_snapshot,conversion_rate,convert
from saed_v4_portfolio_execution_economics.costs import explicit_cost
from saed_v4_portfolio_execution_economics.impact import estimate_impact
from saed_v4_portfolio_execution_economics.dependence import covariance
from saed_v4_portfolio_execution_economics.portfolio import position_metrics
from saed_v4_portfolio_execution_economics.errors import *

def test_direct_fx(fixture):
 s=freeze_fx_snapshot("USD",fixture["fx_rates"],fixture["cutoff_time"]); assert conversion_rate(s,"USD","EUR")==0.92
def test_inverse_fx(fixture):
 s=freeze_fx_snapshot("USD",fixture["fx_rates"],fixture["cutoff_time"]); assert abs(conversion_rate(s,"EUR","USD")-1/0.92)<1e-8
def test_cross_fx(fixture):
 s=freeze_fx_snapshot("USD",fixture["fx_rates"],fixture["cutoff_time"]); assert abs(conversion_rate(s,"GBP","USD")-(1/0.85)*(1/0.92))<1e-6
def test_fx_identity(fixture):
 s=freeze_fx_snapshot("USD",fixture["fx_rates"],fixture["cutoff_time"]); assert convert(s,12.5,"USD","USD")==12.5
def test_explicit_cost_positive(fixture):assert explicit_cost(fixture["cost_schedules"][0],100,12000,2,False)["total_explicit_cost"]>0
def test_short_borrow_more(fixture):
 s=fixture["cost_schedules"][0]; assert explicit_cost(s,1000,120000,10,True)["total_explicit_cost"]>explicit_cost(s,1000,120000,10,False)["total_explicit_cost"]
def test_impact_monotonic(fixture):
 p=fixture["liquidity_profiles"][0]; assert estimate_impact(p,10000,1,.5)["expected_impact_bps"]<estimate_impact(p,40000,1,.5)["expected_impact_bps"]
def test_impact_urgency(fixture):
 p=fixture["liquidity_profiles"][0]; assert estimate_impact(p,10000,1,.1)["expected_impact_bps"]<estimate_impact(p,10000,1,.9)["expected_impact_bps"]
def test_covariance_shape(output):
 c=covariance(output["dependence_model"]); assert len(c)==4 and all(len(r)==4 for r in c)
def test_position_metrics_empty(output):
 p=position_metrics([],output["dependence_model"]); assert p["gross_notional"]==0 and p["portfolio_risk_notional"]==0
