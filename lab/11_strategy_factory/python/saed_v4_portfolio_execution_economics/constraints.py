from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash
from .contracts import require_exact,require_num,require_int,require_time_before
from .errors import PortfolioError

def freeze_constraints(v:dict,cutoff:str)->dict:
    require_exact(v,["constraint_id","base_currency","capital_budget","cash_reserve","gross_limit","net_limit","max_single_instrument_notional","max_single_opportunity_notional","max_cluster_notional","max_portfolio_risk_notional","max_participation_rate","max_depth_multiple","max_order_slices","max_slice_minutes","minimum_net_edge_bps","maximum_expected_cost_bps","known_time","synthetic_fixture"])
    require_time_before(v["known_time"],cutoff,"constraints.known_time")
    for k in ["capital_budget","cash_reserve","gross_limit","net_limit","max_single_instrument_notional","max_single_opportunity_notional","max_cluster_notional","max_portfolio_risk_notional","max_participation_rate","max_depth_multiple","minimum_net_edge_bps","maximum_expected_cost_bps"]: require_num(v[k],k,0)
    require_int(v["max_order_slices"],"max_order_slices",1,64); require_int(v["max_slice_minutes"],"max_slice_minutes",1,240)
    if v["cash_reserve"]>=v["capital_budget"] or v["gross_limit"]>v["capital_budget"]*3: raise PortfolioError("constraint geometry invalid")
    if v["max_participation_rate"]>0.25: raise PortfolioError("participation exceeds constitutional cap")
    body=deepcopy(v); body["constraint_hash"]=content_hash(body); return body
