from __future__ import annotations
from .canonical import seal,hash_chain,q
from .errors import LedgerError

def build_reservation_ledger(allocation:dict,constraints:dict)->dict:
    events=[{"event_type":"CAPITAL_OPEN","amount":float(constraints["capital_budget"]),"opportunity_id":None},{"event_type":"CASH_RESERVE","amount":-float(constraints["cash_reserve"]),"opportunity_id":None}]
    for a in allocation["allocations"]: events.append({"event_type":"SYNTHETIC_RESERVATION","amount":-float(a["allocated_notional"]),"opportunity_id":a["opportunity_id"]})
    chain=hash_chain(events,"v437_reservation_event"); balance=sum(e["amount"] for e in events)
    if balance< -1e-6: raise LedgerError("capital over-reserved")
    return seal({"phase":"SAED_V4_37","events":chain,"event_count":len(chain),"available_balance":float(q(balance)),"synthetic_only":True,"external_account_mutated":False,"research_only":True},"v437_ledger","ledger_id","ledger_hash")
