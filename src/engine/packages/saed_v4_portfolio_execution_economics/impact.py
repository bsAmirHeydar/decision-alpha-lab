from __future__ import annotations
from .canonical import seal,q,dec
from .contracts import require_num
from .errors import ImpactError

def estimate_impact(profile:dict,order_units:float,side:int,urgency:float,confidence:float=0.95)->dict:
    require_num(order_units,"order_units",0.00000001); require_num(urgency,"urgency",0,1); require_num(confidence,"confidence",0.5,0.999)
    if side not in {-1,1}: raise ImpactError("side must be -1 or 1")
    participation=abs(float(order_units))/float(profile["adv_units"])
    if participation>1: raise ImpactError("order exceeds ADV")
    spread=float(profile["median_spread_bps"])/2.0
    root=participation**0.5; vol=float(profile["daily_volatility"])*10000.0
    temporary=(0.14+0.36*urgency)*vol*root
    permanent=0.08*vol*participation
    depth_penalty=max(0.0,abs(float(order_units))/float(profile["depth_units"])-1.0)*spread*0.5
    expected=spread+temporary+permanent+depth_penalty
    band=expected*(1.0+(confidence-0.5)*0.8)
    return seal({"phase":"SAED_V4_37","instrument_id":profile["instrument_id"],"order_units":float(q(order_units)),"side":side,"urgency":float(q(urgency)),"participation_rate":float(q(participation)),"half_spread_bps":float(q(spread)),"temporary_impact_bps":float(q(temporary)),"permanent_impact_bps":float(q(permanent)),"depth_penalty_bps":float(q(depth_penalty)),"expected_impact_bps":float(q(expected)),"upper_impact_bps":float(q(band)),"model":"SYNTHETIC_SQUARE_ROOT_REFERENCE","research_only":True},"v437_impact","estimate_id","estimate_hash")
