from dataclasses import replace
from .contracts import *
from .canonical import *

def make_order(plan,now):
    payload={"plan":plan.plan_id,"signal":plan.signal_id,"volume":plan.sizing.volume,"time":now}
    oid=stable_id("FPORD",payload)
    o=PaperOrder(oid,plan.plan_id,plan.signal_id,OrderState.CREATED,plan.sizing.volume,0.0,0.0,now,now,(),"")
    return replace(o,order_hash=sha256(o))
def transition_order(order,state,now,reason_codes=(),filled_volume=None,average_fill_price=None):
    fv=order.filled_volume if filled_volume is None else filled_volume
    ap=order.average_fill_price if average_fill_price is None else average_fill_price
    valid={
      OrderState.CREATED:{OrderState.VALIDATED,OrderState.REJECTED},
      OrderState.VALIDATED:{OrderState.ATTEMPTED,OrderState.REJECTED},
      OrderState.ATTEMPTED:{OrderState.ACCEPTED,OrderState.REJECTED},
      OrderState.ACCEPTED:{OrderState.PARTIALLY_FILLED,OrderState.FILLED,OrderState.CANCELLED},
      OrderState.PARTIALLY_FILLED:{OrderState.PARTIALLY_FILLED,OrderState.FILLED,OrderState.CANCELLED},
    }
    if state not in valid.get(order.state,set()): raise ValueError(f"illegal order transition {order.state}->{state}")
    o=replace(order,state=state,updated_utc_ms=now,filled_volume=fv,average_fill_price=ap,reason_codes=tuple(sorted(set(order.reason_codes+tuple(reason_codes)))),order_hash="")
    return replace(o,order_hash=sha256(o))
