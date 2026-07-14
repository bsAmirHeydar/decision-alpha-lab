from .contracts import *
from .canonical import *

def _round_stop(value,tick,direction):
    return floor_step(value,tick) if direction==TradeDirection.BUY else ceil_step(value,tick)
def _round_target(value,tick,direction):
    return floor_step(value,tick) if direction==TradeDirection.BUY else ceil_step(value,tick)

def build_geometry(winner:WinnerSignalInput,quote:QuoteSnapshot,spec:SymbolSpec,risk:RiskConfig)->RiskGeometry:
    reasons=[]
    if quote.symbol!=winner.protected_symbol or spec.symbol!=winner.protected_symbol: reasons.append("FP_PAPER_TRADE_SYMBOL_NOT_PROTECTED")
    planned_entry=quote.ask if winner.direction==TradeDirection.BUY else quote.bid
    spread=quote.spread
    raw=winner.raw_structural_stop
    adjusted=raw if winner.direction==TradeDirection.BUY else raw+spread
    adjusted=_round_stop(adjusted,spec.tick_size,winner.direction)
    worst=planned_entry+risk.max_slippage_price if winner.direction==TradeDirection.BUY else planned_entry-risk.max_slippage_price
    if winner.direction==TradeDirection.BUY and adjusted>=planned_entry: reasons.append("FP_PAPER_BUY_STOP_NOT_BELOW_ENTRY")
    if winner.direction==TradeDirection.SELL and adjusted<=planned_entry: reasons.append("FP_PAPER_SELL_STOP_NOT_ABOVE_ENTRY")
    if winner.direction==TradeDirection.SELL and spread<=0: reasons.append("FP_PAPER_SPREAD_SNAPSHOT_UNAVAILABLE")
    distance=abs(worst-adjusted)
    minimum=max(spec.stops_level_price,spec.freeze_level_price,spec.tick_size)
    if distance+1e-12<minimum: reasons.append("FP_PAPER_MINIMUM_STOP_DISTANCE_VIOLATED")
    if distance<=0: reasons.append("FP_PAPER_STOP_DISTANCE_NONPOSITIVE")
    base_distance=abs(planned_entry-adjusted)
    target=planned_entry + (base_distance*risk.target_r_multiple if winner.direction==TradeDirection.BUY else -base_distance*risk.target_r_multiple)
    target=_round_target(target,spec.tick_size,winner.direction)
    if winner.direction==TradeDirection.BUY and target<=planned_entry: reasons.append("FP_PAPER_BUY_TARGET_INVALID")
    if winner.direction==TradeDirection.SELL and target>=planned_entry: reasons.append("FP_PAPER_SELL_TARGET_INVALID")
    status=GeometryStatus.READY if not reasons else GeometryStatus.BLOCKED
    payload={"direction":winner.direction,"symbol":winner.protected_symbol,"quote":quote.quote_id,"entry":planned_entry,"worst":worst,"raw":raw,"spread":spread,"adjusted":adjusted,"target":target,"distance":distance,"minimum":minimum,"risk":risk.config_hash,"reasons":sorted(reasons)}
    gid=stable_id("FPGEO",payload); gh=sha256(payload)
    return RiskGeometry(gid,status,winner.direction,winner.protected_symbol,quote.quote_id,planned_entry,worst,raw,spread,adjusted,target,distance,abs(target-planned_entry),minimum,tuple(sorted(reasons)),gh)
