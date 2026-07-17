from __future__ import annotations
from .canonical import seal,q
from .errors import CapacityError

def compute_capacity(opportunities:dict,liquidity:dict,instruments:dict,prices:dict,constraints:dict)->dict:
    lmap={x["instrument_id"]:x for x in liquidity["profiles"]}; imap={x["instrument_id"]:x for x in instruments["instruments"]}; rows=[]
    for o in opportunities["opportunities"]:
        p=lmap[o["instrument_id"]]; ins=imap[o["instrument_id"]]; price=float(prices[o["instrument_id"]])
        unit_notional=price*float(ins["contract_multiplier"])
        participation_units=float(p["adv_units"])*min(float(p["max_participation_rate"]),float(constraints["max_participation_rate"]))
        depth_units=float(p["depth_units"])*float(constraints["max_depth_multiple"])
        max_units=min(participation_units,depth_units,float(ins["max_lot"]))
        max_notional=max_units*unit_notional
        bound=min(float(o["max_notional"]),max_notional,float(constraints["max_single_opportunity_notional"]))
        rows.append({"opportunity_id":o["opportunity_id"],"instrument_id":o["instrument_id"],"unit_notional":float(q(unit_notional)),"participation_capacity_units":float(q(participation_units)),"depth_capacity_units":float(q(depth_units)),"capacity_units":float(q(max_units)),"capacity_notional":float(q(bound)),"binding_limit":min([("OPPORTUNITY_MAX",float(o["max_notional"])),("LIQUIDITY",max_notional),("SINGLE_OPPORTUNITY",float(constraints["max_single_opportunity_notional"]))],key=lambda x:x[1])[0]})
    return seal({"phase":"SAED_V4_37","rows":rows,"all_bounded":all(x["capacity_notional"]>=0 for x in rows),"research_only":True},"v437_capacity","capacity_id","capacity_hash")
