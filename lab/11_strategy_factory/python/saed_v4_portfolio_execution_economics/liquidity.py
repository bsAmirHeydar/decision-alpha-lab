from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal
from .contracts import require_exact,require_list,require_unique,require_num,require_time_before
from .errors import LiquidityError

def freeze_liquidity_profiles(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"liquidity_profiles",4); require_unique(items,"liquidity_profile_id","liquidity_profiles"); out=[]
    for x in items:
        require_exact(x,["liquidity_profile_id","instrument_id","adv_units","adv_notional","median_spread_bps","daily_volatility","depth_units","max_participation_rate","session_minutes","volume_curve","known_time","synthetic_fixture"])
        require_time_before(x["known_time"],cutoff,"liquidity.known_time")
        for k in ["adv_units","adv_notional","median_spread_bps","daily_volatility","depth_units","max_participation_rate","session_minutes"]: require_num(x[k],k,0.00000001)
        if x["max_participation_rate"]>0.25: raise LiquidityError("participation cap exceeds constitution")
        curve=require_list(x["volume_curve"],"volume_curve",4)
        if abs(sum(float(v) for v in curve)-1.0)>1e-9 or any(float(v)<=0 for v in curve): raise LiquidityError("volume curve must be positive and sum to one")
        y=deepcopy(x); y["profile_hash"]=content_hash(y); out.append(y)
    return seal({"phase":"SAED_V4_37","cutoff_time":cutoff,"profiles":sorted(out,key=lambda x:x["instrument_id"]),"research_only":True},"v437_liquidity","registry_id","registry_hash")

def liquidity_map(registry:dict)->dict:return {x["instrument_id"]:x for x in registry["profiles"]}
