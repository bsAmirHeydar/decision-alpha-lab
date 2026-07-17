from __future__ import annotations
from copy import deepcopy
from .contracts import exact,number,integer
from .errors import RiskError
from .canonical import content_hash,seal,q

def freeze_risk_envelope(v:dict)->dict:
 exact(v,["risk_envelope_id","version","max_trade_risk_fraction","max_daily_loss_fraction","max_gross_notional_fraction","max_concurrent_positions","max_orders_per_day","max_spread_bps","max_slippage_bps","max_latency_ms","max_reject_rate","max_drawdown_fraction","cooldown_bars_after_loss","kill_switch_default_armed","position_size_hard_cap","research_only"])
 for k in ["max_trade_risk_fraction","max_daily_loss_fraction","max_gross_notional_fraction","max_reject_rate","max_drawdown_fraction","position_size_hard_cap"]:number(v[k],k,0,1)
 for k in ["max_spread_bps","max_slippage_bps"]:number(v[k],k,0,1000)
 integer(v["max_latency_ms"],"max_latency_ms",1,60000);integer(v["max_concurrent_positions"],"max_concurrent_positions",1,100);integer(v["max_orders_per_day"],"max_orders_per_day",1,1000);integer(v["cooldown_bars_after_loss"],"cooldown_bars_after_loss",0,1000)
 if v["kill_switch_default_armed"] is not True or v["research_only"] is not True:raise RiskError("risk boundary invalid")
 x=deepcopy(v);x["risk_envelope_hash"]=content_hash(x);return seal(x,"v439_risk","frozen_risk_id","frozen_risk_hash")

def evaluate_intent(intent:dict,envelope:dict,state:dict)->dict:
 reasons=[]
 if float(intent["risk_fraction"])>float(envelope["max_trade_risk_fraction"]):reasons.append("TRADE_RISK_CAP")
 if float(intent["size_fraction"])>float(envelope["position_size_hard_cap"]):reasons.append("SIZE_CAP")
 if float(intent["spread_bps"])>float(envelope["max_spread_bps"]):reasons.append("SPREAD_CAP")
 if float(intent["latency_ms"])>float(envelope["max_latency_ms"]):reasons.append("LATENCY_CAP")
 if state["orders_today"]>=envelope["max_orders_per_day"]:reasons.append("ORDER_COUNT_CAP")
 if state["concurrent_positions"]>=envelope["max_concurrent_positions"]:reasons.append("CONCURRENCY_CAP")
 if float(state["daily_loss_fraction"])>=float(envelope["max_daily_loss_fraction"]):reasons.append("DAILY_LOSS_CAP")
 if float(state["drawdown_fraction"])>=float(envelope["max_drawdown_fraction"]):reasons.append("DRAWDOWN_CAP")
 if state["kill_switch_armed"] is not True:reasons.append("KILL_SWITCH_NOT_ARMED")
 passed=not reasons
 return seal({"intent_id":intent["intent_id"],"passed":passed,"reasons":sorted(reasons),"approved_size_fraction":q(intent["size_fraction"]) if passed else 0.0,"order_submission_allowed":False,"capital_activation_allowed":False,"research_only":True},"v439_risk_decision","risk_decision_id","risk_decision_hash")
