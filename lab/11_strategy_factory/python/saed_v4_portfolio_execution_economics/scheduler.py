from __future__ import annotations
import math
from .canonical import seal,q
from .errors import SchedulingError

def build_non_executable_schedule(allocation:dict,opportunities:dict,instruments:dict,liquidity:dict,prices:dict,constraints:dict)->dict:
    omap={x["opportunity_id"]:x for x in opportunities["opportunities"]}; imap={x["instrument_id"]:x for x in instruments["instruments"]}; lmap={x["instrument_id"]:x for x in liquidity["profiles"]}; orders=[]
    for a in allocation["allocations"]:
        o=omap[a["opportunity_id"]]; ins=imap[a["instrument_id"]]; prof=lmap[a["instrument_id"]]; unit_notional=float(prices[a["instrument_id"]])*float(ins["contract_multiplier"]); units=float(a["allocated_notional"])/unit_notional
        max_units_per_slice=float(prof["adv_units"])*float(constraints["max_participation_rate"])/len(prof["volume_curve"])
        slices=min(int(constraints["max_order_slices"]),max(1,math.ceil(units/max(max_units_per_slice,1e-12))))
        curve=prof["volume_curve"][:slices]; denom=sum(curve); remaining=units; rows=[]
        for i,v in enumerate(curve):
            qty=remaining if i==len(curve)-1 else units*float(v)/denom; remaining-=qty
            rows.append({"slice_index":i,"planned_units":float(q(qty)),"window_minutes":int(constraints["max_slice_minutes"]),"max_participation_rate":float(constraints["max_participation_rate"]),"order_type":"PASSIVE_LIMIT_REFERENCE" if i<max(1,len(curve)-1) else "LIMIT_REFERENCE","executable":False})
        orders.append({"opportunity_id":a["opportunity_id"],"instrument_id":a["instrument_id"],"direction":a["direction"],"total_units":float(q(units)),"slice_count":len(rows),"slices":rows,"status":"NOT_SUBMITTED","broker_route":None,"runtime_authorized":False})
    return seal({"phase":"SAED_V4_37","orders":orders,"order_count":len(orders),"all_non_executable":all(not s["executable"] for o in orders for s in o["slices"]),"order_submission_allowed":False,"research_only":True},"v437_schedule","schedule_id","schedule_hash")
