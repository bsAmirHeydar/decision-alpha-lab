from __future__ import annotations
from .canonical import q,seal,hash_chain
from .errors import PaperError

def simulate(intents:list[dict],observations:list[dict],risk_decisions:list[dict],broker:dict)->dict:
 obs={x["observation_id"]:x for x in observations};risk={x["intent_id"]:x for x in risk_decisions};events=[];pnl=0.0;filled=0;rejected=0
 for intent in intents:
  o=obs[intent["observation_id"]];r=risk[intent["intent_id"]]
  status="ABSTAIN";fill_price=0.0;slippage=0.0;gross=0.0;cost=0.0;net=0.0
  if intent["decision"]=="SELECT":
   if not r["passed"]:status="RISK_REJECTED";rejected+=1
   else:
    status="PAPER_FILLED";filled+=1
    entry=float(o["ask"] if intent["side"]=="BUY" else o["bid"])
    exitp=float(o["next_bid"] if intent["side"]=="BUY" else o["next_ask"])
    direction=1.0 if intent["side"]=="BUY" else -1.0
    slippage=min(float(intent["spread_bps"])*.15,float(intent["latency_ms"])/1000*.2)
    fill_price=entry*(1+(slippage/10000)*direction)
    gross=direction*(exitp-fill_price)/max(1e-12,fill_price)*10000
    cost=float(o["expected_cost_bps"])+slippage;net=gross-cost;pnl+=net
  events.append({"observation_id":o["observation_id"],"intent_id":intent["intent_id"],"known_time":o["known_time"],"mode":"PAPER","status":status,"side":intent["side"],"fill_price":q(fill_price),"slippage_bps":q(slippage),"gross_pnl_bps":q(gross),"cost_bps":q(cost),"net_pnl_bps":q(net),"broker_side_effect":False,"order_submitted":False,"synthetic_fixture":True,"research_only":True})
 count=max(1,filled);metrics={"observation_count":len(observations),"selected_count":sum(x["decision"]=="SELECT" for x in intents),"filled_count":filled,"rejected_count":rejected,"abstained_count":sum(x["decision"]!="SELECT" for x in intents),"mean_net_pnl_bps":q(pnl/count),"cumulative_net_pnl_bps":q(pnl),"order_submission_count":0,"broker_side_effect_count":0}
 return seal({"phase":"SAED_V4_39","mode":"PAPER","events":hash_chain(events,"v439_paper_event"),"metrics":metrics,"prospective":True,"research_only":True,"production_authorized":False},"v439_paper","ledger_id","ledger_hash")
