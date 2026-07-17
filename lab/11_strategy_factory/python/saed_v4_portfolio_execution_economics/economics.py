from __future__ import annotations
from .canonical import seal,q
from .costs import explicit_cost
from .impact import estimate_impact

def opportunity_economics(opportunities:dict,capacity:dict,instruments:dict,liquidity:dict,costs:dict,prices:dict,constraints:dict)->dict:
    imap={x["instrument_id"]:x for x in instruments["instruments"]}; lmap={x["instrument_id"]:x for x in liquidity["profiles"]}; cmap={x["instrument_id"]:x for x in costs["schedules"]}; capmap={x["opportunity_id"]:x for x in capacity["rows"]}; rows=[]
    for o in opportunities["opportunities"]:
        ins=imap[o["instrument_id"]]; price=float(prices[o["instrument_id"]]); unit_notional=price*float(ins["contract_multiplier"])
        notional=min(float(o["requested_notional"]),float(capmap[o["opportunity_id"]]["capacity_notional"])); units=notional/unit_notional if unit_notional else 0.0
        explicit=explicit_cost(cmap[o["instrument_id"]],units,notional,float(o["holding_days"]),o["direction"]=="SHORT")
        impact=estimate_impact(lmap[o["instrument_id"]],max(units,0.00000001),o["direction_sign"],1-float(o["confidence"])*0.5)
        explicit_bps=float(explicit["total_explicit_cost"])/notional*10000 if notional else 0.0
        expected_cost=explicit_bps+float(impact["expected_impact_bps"]); upper_cost=explicit_bps+float(impact["upper_impact_bps"])
        gross=float(o["expected_gross_bps"]); net=gross-expected_cost; conservative=gross-upper_cost
        eligible=notional>0 and net>=float(constraints["minimum_net_edge_bps"]) and expected_cost<=float(constraints["maximum_expected_cost_bps"])
        rows.append({"opportunity_id":o["opportunity_id"],"context_id":o["context_id"],"treatment_id":o["treatment_id"],"instrument_id":o["instrument_id"],"direction":o["direction"],"candidate_notional":float(q(notional)),"candidate_units":float(q(units)),"expected_gross_bps":float(q(gross)),"explicit_cost_bps":float(q(explicit_bps)),"expected_impact_bps":impact["expected_impact_bps"],"upper_impact_bps":impact["upper_impact_bps"],"expected_total_cost_bps":float(q(expected_cost)),"upper_total_cost_bps":float(q(upper_cost)),"expected_net_edge_bps":float(q(net)),"conservative_net_edge_bps":float(q(conservative)),"break_even_gross_bps":float(q(expected_cost)),"eligible":eligible,"rejection_reason":None if eligible else "ECONOMICS_GATE_FAILED"})
    return seal({"phase":"SAED_V4_37","rows":rows,"eligible_count":sum(x["eligible"] for x in rows),"research_only":True},"v437_economics","economics_id","economics_hash")
