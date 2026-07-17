from __future__ import annotations
from collections import defaultdict
from .canonical import seal,q
from .portfolio import position_metrics
from .errors import AllocationError

def allocate(economics:dict,opportunities:dict,dependence:dict,constraints:dict)->dict:
    omap={x["opportunity_id"]:x for x in opportunities["opportunities"]}; ranked=[]
    for e in economics["rows"]:
        o=omap[e["opportunity_id"]]
        score=float(e["conservative_net_edge_bps"])*float(o["confidence"])*float(o["signal_strength"])
        ranked.append((score,e["opportunity_id"],e,o))
    ranked.sort(key=lambda x:(-x[0],x[1])); gross=0.0; net=0.0; by_inst=defaultdict(float); by_cluster=defaultdict(float); allocations=[]; rejections=[]
    deployable=float(constraints["capital_budget"])-float(constraints["cash_reserve"])
    for score,oid,e,o in ranked:
        if not e["eligible"]: rejections.append({"opportunity_id":oid,"reason":"ECONOMICS_GATE_FAILED"}); continue
        requested=float(e["candidate_notional"]); sign=1 if o["direction"]=="LONG" else -1
        limits=[requested,deployable-gross,float(constraints["gross_limit"])-gross,float(constraints["max_single_instrument_notional"])-by_inst[o["instrument_id"]],float(constraints["max_cluster_notional"])-by_cluster[o["strategy_cluster"]]]
        net_room=float(constraints["net_limit"])-abs(net)
        limits.append(net_room)
        amount=max(0.0,min(limits))
        if amount<=0: rejections.append({"opportunity_id":oid,"reason":"PORTFOLIO_CONSTRAINT_BINDING"}); continue
        allocations.append({"opportunity_id":oid,"context_id":o["context_id"],"treatment_id":o["treatment_id"],"instrument_id":o["instrument_id"],"direction":o["direction"],"strategy_cluster":o["strategy_cluster"],"allocated_notional":float(q(amount)),"score":float(q(score)),"expected_net_edge_bps":e["expected_net_edge_bps"],"conservative_net_edge_bps":e["conservative_net_edge_bps"]})
        gross+=amount; net+=sign*amount; by_inst[o["instrument_id"]]+=amount; by_cluster[o["strategy_cluster"]]+=amount
    snap=position_metrics(allocations,dependence)
    if snap["portfolio_risk_notional"]>float(constraints["max_portfolio_risk_notional"]):
        scale=float(constraints["max_portfolio_risk_notional"])/snap["portfolio_risk_notional"]
        for a in allocations:a["allocated_notional"]=float(q(a["allocated_notional"]*scale))
        snap=position_metrics(allocations,dependence)
    return seal({"phase":"SAED_V4_37","allocations":allocations,"rejections":sorted(rejections,key=lambda x:x["opportunity_id"]),"portfolio_snapshot":snap,"baseline_preserved":True,"optimization":"DETERMINISTIC_CONSTRAINED_GREEDY_REFERENCE","research_only":True},"v437_allocation","plan_id","plan_hash")
