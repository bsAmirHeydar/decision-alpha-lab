from __future__ import annotations
import math
from .contracts import OpportunityCandidate,CapacityQuote
from .canonical import canonical_sha256

def estimate_capacity(candidate:OpportunityCandidate,known_time_ms:int,market_open:bool=True,spread_bps:float=1.0,base_depth:float=10.0,impact_coefficient:float=0.25,broker_volume_step:float=0.01):
    if spread_bps<0 or base_depth<=0 or impact_coefficient<0 or broker_volume_step<=0: raise ValueError('invalid capacity inputs')
    raw=min(candidate.capacity_units,base_depth*candidate.liquidity_score)
    fill=0.0 if not market_open else min(1.0,raw/max(candidate.requested_risk,1e-12))
    impact=impact_coefficient*(candidate.requested_risk/max(raw,1e-12))**2
    maxrisk=math.floor(raw/broker_volume_step)*broker_volume_step if market_open else 0.0
    degraded=max(0.0,candidate.utility_mean-spread_bps/10000-impact/10000)
    src=canonical_sha256({'candidate':candidate.candidate_hash,'spread':spread_bps,'depth':base_depth,'impact':impact_coefficient,'step':broker_volume_step,'open':market_open})
    return CapacityQuote(quote_id='capacity:'+candidate.candidate_id,candidate_id=candidate.candidate_id,known_time_ms=known_time_ms,max_risk_units=maxrisk,expected_fill_ratio=fill,spread_bps=spread_bps,impact_bps=impact,degraded_utility=degraded,broker_volume_step=broker_volume_step,market_open=market_open,source_hash=src)
