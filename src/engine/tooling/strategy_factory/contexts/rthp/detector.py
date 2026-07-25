from __future__ import annotations
from .identity import stable_event_id
VALID="VALID"
def evaluate_divergence(req:dict)->dict:
 if int(req.get("available_reference_count",0))==0:
  return {"evaluation_status":"INSUFFICIENT_HISTORY","event_created":False,"polarity":None,"data_sufficiency":"NONE"}
 if req.get("price_basis_primary")!=req.get("price_basis_secondary"):
  return {"evaluation_status":"INVALID_PRICE_BASIS_MISMATCH","event_created":False,"polarity":None}
 p=req["primary"];s=req["secondary"]
 if p.get("data_status")!=VALID or s.get("data_status")!=VALID:
  return {"evaluation_status":"UNCONFIRMED","event_created":False,"polarity":None,"confirmed_context_event":False,"re_evaluation_required":True}
 pt=bool(p.get("touched"));st=bool(s.get("touched"))
 suff="FULL" if int(req.get("available_reference_count",0))>=int(req.get("required_reference_count",0)) else "PARTIAL"
 if pt==st:return {"evaluation_status":"NO_EVENT","event_created":False,"polarity":None,"data_sufficiency":suff}
 hunter=p if pt else s; protected=s if pt else p
 enriched=dict(req);enriched["hunter_symbol"]=hunter["symbol"];enriched["protected_symbol"]=protected["symbol"];enriched["first_touch_time"]=hunter.get("first_touch_time")
 polarity="BEARISH_DIVERGENCE" if req["level_side"]=="HIGH" else "BULLISH_DIVERGENCE"
 return {"evaluation_status":"CONFIRMED","event_created":True,"polarity":polarity,"event_id":stable_event_id(enriched),"hunter_symbol":hunter["symbol"],"protected_symbol":protected["symbol"],"data_sufficiency":suff,"confirmed_context_event":True}
