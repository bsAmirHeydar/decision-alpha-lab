from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal
from .contracts import require_exact,require_list,require_unique,require_num,require_int,require_enum,require_time_before
from .errors import InstrumentError

KINDS={"FUTURE","EQUITY","ETF","FX","CFD","INDEX_PROXY"}

def freeze_instrument_master(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"instruments",4); require_unique(items,"instrument_id","instruments"); out=[]
    for x in items:
        require_exact(x,["instrument_id","symbol","kind","quote_currency","settlement_currency","tick_size","tick_value","contract_multiplier","lot_step","min_lot","max_lot","margin_rate","shortable","known_time","synthetic_fixture"])
        require_enum(x["kind"],KINDS,"kind"); require_time_before(x["known_time"],cutoff,"instrument.known_time")
        for k in ["tick_size","tick_value","contract_multiplier","lot_step","min_lot","max_lot"]: require_num(x[k],k,0.00000001)
        require_num(x["margin_rate"],"margin_rate",0,1)
        if x["min_lot"]>x["max_lot"] or x["lot_step"]>x["max_lot"]: raise InstrumentError("lot bounds invalid")
        y=deepcopy(x); y["instrument_hash"]=content_hash(y); out.append(y)
    return seal({"phase":"SAED_V4_37","cutoff_time":cutoff,"instruments":sorted(out,key=lambda x:x["instrument_id"]),"instrument_count":len(out),"research_only":True},"v437_instruments","master_id","master_hash")

def instrument_map(master:dict)->dict:return {x["instrument_id"]:x for x in master["instruments"]}
