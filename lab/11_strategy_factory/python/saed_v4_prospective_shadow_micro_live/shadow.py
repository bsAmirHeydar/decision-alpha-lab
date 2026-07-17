from __future__ import annotations
from .canonical import q,seal,hash_chain

def run(intents:list[dict],observations:list[dict],paper:dict)->dict:
 p={x["observation_id"]:x for x in paper["events"]};events=[];agree=0;selected=0
 for intent,o in zip(intents,observations):
  baseline=o["baseline_decision"];shadow=intent["decision"];a=baseline==shadow;agree+=int(a);selected+=int(shadow=="SELECT")
  events.append({"observation_id":o["observation_id"],"intent_id":intent["intent_id"],"known_time":o["known_time"],"mode":"SHADOW","shadow_decision":shadow,"baseline_decision":baseline,"agreement":a,"paper_status":p[o["observation_id"]]["status"],"paper_net_pnl_bps":p[o["observation_id"]]["net_pnl_bps"],"order_submitted":False,"broker_side_effect":False,"counterfactual_only":True,"synthetic_fixture":True,"research_only":True})
 n=max(1,len(events));metrics={"observation_count":len(events),"selected_count":selected,"agreement_rate":q(agree/n),"disagreement_rate":q(1-agree/n),"order_submission_count":0,"broker_side_effect_count":0,"future_suffix_used":False}
 return seal({"phase":"SAED_V4_39","mode":"SHADOW","events":hash_chain(events,"v439_shadow_event"),"metrics":metrics,"prospective":True,"research_only":True,"production_authorized":False},"v439_shadow","ledger_id","ledger_hash")
