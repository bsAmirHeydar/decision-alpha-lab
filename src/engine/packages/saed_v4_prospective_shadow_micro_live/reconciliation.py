from __future__ import annotations
from .canonical import q,seal,hash_chain
from .errors import ReconciliationError

def reconcile(intents:list[dict],paper:dict)->dict:
 events=[];paper_by={x["intent_id"]:x for x in paper["events"]};unmatched=[]
 for i in intents:
  p=paper_by.get(i["intent_id"])
  if p is None:unmatched.append(i["intent_id"]);continue
  events.append({"intent_id":i["intent_id"],"observation_id":i["observation_id"],"intent_decision":i["decision"],"paper_status":p["status"],"quantity_match":True,"price_reconciled":p["status"]!="PAPER_FILLED" or p["fill_price"]>0,"live_order_id":None,"live_fill_id":None,"cash_delta":0.0,"position_delta":0.0,"reconciled":True,"research_only":True})
 if unmatched:raise ReconciliationError(f"unmatched intents {unmatched}")
 return seal({"phase":"SAED_V4_39","events":hash_chain(events,"v439_reconciliation_event"),"intent_count":len(intents),"reconciled_count":len(events),"unmatched_count":0,"live_order_count":0,"live_fill_count":0,"cash_delta":q(0),"position_delta":q(0),"research_only":True},"v439_reconciliation","ledger_id","ledger_hash")
