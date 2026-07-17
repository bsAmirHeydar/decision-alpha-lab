from __future__ import annotations
from typing import Any
from .canonical import digest_object, stable_id
from .errors import IntegrityError

class EventLedger:
    def __init__(self,batch_seed: str):
        self.batch_seed=batch_seed; self.events=[]; self.previous=None
    def append(self,event_type: str,payload: dict[str,Any],occurred_at: str) -> dict[str,Any]:
        seq=len(self.events)+1
        body={"schema_version":"1.0.0","event_id":stable_id("BATCH_EVENT",self.batch_seed,str(seq),event_type),"sequence":seq,"event_type":event_type,"occurred_at":occurred_at,"previous_event_digest":self.previous,"payload":payload,"live_order_submission_allowed":False,"capital_activation_allowed":False}
        event={**body,"event_digest":digest_object(body)}; self.events.append(event); self.previous=event["event_digest"]; return event
    def document(self) -> dict[str,Any]:
        body={"schema_version":"1.0.0","event_count":len(self.events),"first_event_digest":self.events[0]["event_digest"] if self.events else None,"last_event_digest":self.previous,"events":self.events,"hash_chain_complete":True}
        return {**body,"ledger_digest":digest_object(body)}

def verify_event_ledger(doc: dict[str,Any]) -> bool:
    previous=None
    for index,event in enumerate(doc.get("events",[]),1):
        if event.get("sequence")!=index or event.get("previous_event_digest")!=previous: return False
        if event.get("event_digest")!=digest_object({k:v for k,v in event.items() if k!="event_digest"}): return False
        previous=event["event_digest"]
    body={k:v for k,v in doc.items() if k!="ledger_digest"}
    return doc.get("event_count")==len(doc.get("events",[])) and doc.get("last_event_digest")==previous and doc.get("ledger_digest")==digest_object(body)
