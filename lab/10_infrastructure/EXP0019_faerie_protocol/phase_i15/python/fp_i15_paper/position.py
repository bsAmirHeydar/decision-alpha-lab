from dataclasses import replace
from .contracts import *
from .canonical import *

def position_from_fills(plan,order,fills,now):
    volume=sum(f.volume for f in fills)
    avg=sum(f.volume*f.price for f in fills)/volume
    payload={"order":order.order_id,"plan":plan.plan_id,"volume":volume,"avg":avg,"stop":plan.geometry.adjusted_stop,"target":plan.geometry.target}
    pid=stable_id("FPPOS",payload)
    p=PaperPosition(pid,order.order_id,plan.plan_id,plan.trade_symbol,plan.direction,volume,avg,plan.geometry.adjusted_stop,plan.geometry.target,PositionState.OPEN,now,position_hash="")
    return replace(p,position_hash=sha256(p))
def close_position(position,spec,close_price,now,state):
    ticks=(close_price-position.average_entry)/spec.tick_size
    if position.direction==TradeDirection.SELL: ticks=-ticks
    pnl=ticks*spec.tick_value_loss_per_lot*position.volume
    p=replace(position,state=state,closed_utc_ms=now,close_price=close_price,realized_pnl=pnl,position_hash="")
    return replace(p,position_hash=sha256(p))
