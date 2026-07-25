from __future__ import annotations
from copy import deepcopy
from .canonical import seal,q
from .contracts import require_exact,require_list,require_unique,require_num
from .errors import StressError

def run_stress(allocation:dict,economics:dict,scenarios:list[dict],constraints:dict)->dict:
    scenarios=require_list(scenarios,"stress_scenarios",5); require_unique(scenarios,"scenario_id","stress_scenarios"); scenarios=sorted(scenarios,key=lambda x:x["scenario_id"]); emap={x["opportunity_id"]:x for x in economics["rows"]}; rows=[]
    for s in scenarios:
        require_exact(s,["scenario_id","cost_multiplier","edge_multiplier","liquidity_multiplier","correlation_multiplier","funding_add_bps","fill_ratio","synthetic_fixture"])
        for k in ["cost_multiplier","edge_multiplier","liquidity_multiplier","correlation_multiplier","fill_ratio"]: require_num(s[k],k,0)
        require_num(s["funding_add_bps"],"funding_add_bps",0)
        gross=cost=0.0
        for a in allocation["allocations"]:
            e=emap[a["opportunity_id"]]; n=float(a["allocated_notional"])*float(s["fill_ratio"])*min(1.0,float(s["liquidity_multiplier"]))
            gross+=n*float(e["expected_gross_bps"])*float(s["edge_multiplier"])/10000
            cost+=n*(float(e["expected_total_cost_bps"])*float(s["cost_multiplier"])+float(s["funding_add_bps"]))/10000
        pnl=gross-cost; risk=float(allocation["portfolio_snapshot"]["portfolio_risk_notional"])*float(s["correlation_multiplier"])
        passed=pnl>=-float(constraints["capital_budget"])*0.02 and risk<=float(constraints["max_portfolio_risk_notional"])*1.5
        rows.append({"scenario_id":s["scenario_id"],"stressed_gross_value":float(q(gross)),"stressed_cost_value":float(q(cost)),"stressed_net_value":float(q(pnl)),"stressed_risk_notional":float(q(risk)),"passed":passed})
    return seal({"phase":"SAED_V4_37","rows":rows,"scenario_count":len(rows),"all_passed":all(x["passed"] for x in rows),"worst_net_value":min(x["stressed_net_value"] for x in rows),"research_only":True},"v437_stress","suite_id","suite_hash")
