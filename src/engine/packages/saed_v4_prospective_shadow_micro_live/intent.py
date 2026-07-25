from __future__ import annotations
from copy import deepcopy
from .contracts import exact,enum,number
from .errors import IntentError
from .canonical import seal,hash_chain,q
SIDES={"BUY","SELL","NONE"};DECISIONS={"SELECT","ABSTAIN"}
def build_intent(obs:dict,runtime_binding:dict)->dict:
 exact(obs,["observation_id","known_time","context_id","instrument","decision","side","signal_score","expected_edge_bps","expected_cost_bps","bid","ask","bar_high","bar_low","next_bid","next_ask","latency_ms","baseline_decision","synthetic_fixture"])
 enum(obs["decision"],DECISIONS,"decision");enum(obs["side"],SIDES,"side")
 spread=max(0.0,(float(obs["ask"])-float(obs["bid"]))/max(1e-12,(float(obs["ask"])+float(obs["bid"]))/2)*10000)
 selected=obs["decision"]=="SELECT" and obs["side"] in {"BUY","SELL"}
 size=max(0.0,min(.01,float(obs["signal_score"])*.01)) if selected else 0.0
 risk=size*.5
 body={"observation_id":obs["observation_id"],"known_time":obs["known_time"],"context_id":obs["context_id"],"instrument":obs["instrument"],"decision":obs["decision"],"side":obs["side"] if selected else "NONE","reference_price":q(obs["ask"] if obs["side"]=="BUY" else obs["bid"]),"size_fraction":q(size),"risk_fraction":q(risk),"spread_bps":q(spread),"latency_ms":int(obs["latency_ms"]),"runtime_bundle_hash":runtime_binding["bundle_hash"],"submission_mode":"INTENT_ONLY","submission_allowed":False,"capital_activation_allowed":False,"synthetic_fixture":True,"research_only":True}
 return seal(body,"v439_intent","intent_id","intent_hash")
def intent_ledger(intents:list[dict])->dict:
 return seal({"phase":"SAED_V4_39","events":hash_chain(intents,"v439_intent_event"),"intent_count":len(intents),"submission_count":0,"research_only":True},"v439_intent_ledger","ledger_id","ledger_hash")
