from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal,q,dec
from .contracts import require_exact,require_list,require_unique,require_num,require_enum,require_time_before
from .errors import CostError

MODES={"PER_UNIT","PER_NOTIONAL_BPS","FLAT"}

def freeze_cost_schedules(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"cost_schedules",4); require_unique(items,"cost_schedule_id","cost_schedules"); out=[]
    for x in items:
        require_exact(x,["cost_schedule_id","instrument_id","commission_mode","commission_value","exchange_fee_per_unit","regulatory_fee_bps","borrow_bps_annual","funding_bps_annual","tax_bps","minimum_fee","known_time","synthetic_fixture"])
        require_enum(x["commission_mode"],MODES,"commission_mode"); require_time_before(x["known_time"],cutoff,"cost.known_time")
        for k in ["commission_value","exchange_fee_per_unit","regulatory_fee_bps","borrow_bps_annual","funding_bps_annual","tax_bps","minimum_fee"]: require_num(x[k],k,0)
        y=deepcopy(x); y["schedule_hash"]=content_hash(y); out.append(y)
    return seal({"phase":"SAED_V4_37","cutoff_time":cutoff,"schedules":sorted(out,key=lambda x:x["instrument_id"]),"research_only":True},"v437_costs","registry_id","registry_hash")

def explicit_cost(schedule:dict,units:float,notional:float,holding_days:float,is_short:bool)->dict:
    u=abs(dec(units)); n=abs(dec(notional)); mode=schedule["commission_mode"]
    if mode=="PER_UNIT": commission=u*dec(schedule["commission_value"])
    elif mode=="PER_NOTIONAL_BPS": commission=n*dec(schedule["commission_value"])/dec(10000)
    else: commission=dec(schedule["commission_value"])
    exchange=u*dec(schedule["exchange_fee_per_unit"]); regulatory=n*dec(schedule["regulatory_fee_bps"])/dec(10000)
    carry_bps=dec(schedule["funding_bps_annual"])+(dec(schedule["borrow_bps_annual"]) if is_short else dec(0))
    carry=n*carry_bps*dec(holding_days)/dec(3650000); tax=n*dec(schedule["tax_bps"])/dec(10000)
    subtotal=commission+exchange+regulatory+carry+tax; total=max(subtotal,dec(schedule["minimum_fee"]))
    return {"commission":float(q(commission)),"exchange_fee":float(q(exchange)),"regulatory_fee":float(q(regulatory)),"carry":float(q(carry)),"tax":float(q(tax)),"minimum_fee_applied":total>subtotal,"total_explicit_cost":float(q(total))}
