from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id

def build_event_ledger(validation_id:str,events:list[tuple[str,dict[str,Any]]],occurred_at:str)->dict[str,Any]:
    prev='GENESIS'; rows=[]
    for seq,(etype,payload) in enumerate(events,1):
        body={'schema_version':'1.0.0','sequence':seq,'event_id':stable_id('VALEVT',validation_id,str(seq),etype),'event_type':etype,'occurred_at':occurred_at,'previous_event_digest':prev,'payload':payload,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        row={**body,'event_digest':digest_object(body)}; rows.append(row); prev=row['event_digest']
    body={'schema_version':'1.0.0','validation_id':validation_id,'event_count':len(rows),'events':rows,'terminal_event_digest':prev}
    return {**body,'ledger_digest':digest_object(body)}
def verify_event_ledger(doc:dict[str,Any])->bool:
    prev='GENESIS'
    for i,row in enumerate(doc.get('events',[]),1):
        if row.get('sequence')!=i or row.get('previous_event_digest')!=prev: return False
        body={k:v for k,v in row.items() if k!='event_digest'}
        if row.get('event_digest')!=digest_object(body): return False
        prev=row['event_digest']
    body={k:v for k,v in doc.items() if k!='ledger_digest'}
    return doc.get('event_count')==len(doc.get('events',[])) and doc.get('terminal_event_digest')==prev and doc.get('ledger_digest')==digest_object(body)
