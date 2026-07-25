from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal,q,dec
from .contracts import require_exact,require_list,require_unique,require_num,require_enum,require_time_before
from .errors import PortfolioError

DIRECTIONS={"LONG":1,"SHORT":-1}

def freeze_opportunities(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"opportunities",6); require_unique(items,"opportunity_id","opportunities"); out=[]
    for x in items:
        require_exact(x,["opportunity_id","context_id","treatment_id","instrument_id","direction","expected_gross_bps","confidence","signal_strength","holding_days","requested_notional","max_notional","strategy_cluster","known_time","synthetic_fixture"])
        require_enum(x["direction"],set(DIRECTIONS),"direction"); require_time_before(x["known_time"],cutoff,"opportunity.known_time")
        require_num(x["confidence"],"confidence",0,1); require_num(x["signal_strength"],"signal_strength",0,1); require_num(x["holding_days"],"holding_days",0.0001)
        require_num(x["requested_notional"],"requested_notional",0); require_num(x["max_notional"],"max_notional",0)
        if x["requested_notional"]>x["max_notional"]: raise PortfolioError("requested notional above opportunity maximum")
        y=deepcopy(x); y["direction_sign"]=DIRECTIONS[x["direction"]]; y["opportunity_hash"]=content_hash(y); out.append(y)
    return seal({"phase":"SAED_V4_37","cutoff_time":cutoff,"opportunities":sorted(out,key=lambda x:x["opportunity_id"]),"research_only":True},"v437_opportunities","registry_id","registry_hash")

def position_metrics(allocations:list[dict],dep:dict)->dict:
    ids=dep["instrument_ids"]; index={x:i for i,x in enumerate(ids)}; signed={x:0.0 for x in ids}
    gross=0.0
    for a in allocations:
        s=float(a["allocated_notional"])*(1 if a["direction"]=="LONG" else -1); signed[a["instrument_id"]]+=s; gross+=abs(s)
    net=sum(signed.values()); cov=[]
    for i,a in enumerate(ids):
        row=[]
        for j,b in enumerate(ids): row.append(float(dep["correlation_matrix"][i][j])*float(dep["volatility_vector"][a])*float(dep["volatility_vector"][b]))
        cov.append(row)
    variance=0.0
    for a in ids:
        for b in ids: variance+=signed[a]*signed[b]*cov[index[a]][index[b]]
    risk=max(0.0,variance)**0.5
    return seal({"phase":"SAED_V4_37","gross_notional":float(q(gross)),"net_notional":float(q(net)),"signed_notional_by_instrument":{k:float(q(v)) for k,v in sorted(signed.items())},"portfolio_risk_notional":float(q(risk)),"allocation_count":len(allocations),"research_only":True},"v437_portfolio","snapshot_id","snapshot_hash")
