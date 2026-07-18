from __future__ import annotations
from .canonical import content_id, digest_object
from .errors import IntegrityError

def build(events: list[tuple[str,dict]], occurred_at: str) -> dict:
    previous='sha256:'+'0'*64; rows=[]
    for i,(typ,payload) in enumerate(events,1):
        e={'sequence':i,'event_id':content_id('LCM01EVT',{'sequence':i,'type':typ,'payload':payload}),'event_type':typ,'occurred_at':occurred_at,'previous_event_digest':previous,'payload':payload,'source_move_authority':False,'source_delete_authority':False,'semantic_refactor_authority':False,'runtime_authority':False,'live_order_authority':False,'capital_authority':False,'event_digest':''}
        e['event_digest']=digest_object(e,'event_digest'); previous=e['event_digest']; rows.append(e)
    ledger={'schema_version':'1.0.0','phase_id':'LCM-01','events':rows,'event_count':len(rows),'head_digest':previous,'ledger_digest':''}
    ledger['ledger_digest']=digest_object(ledger,'ledger_digest'); return ledger

def verify(value: dict) -> None:
    if value.get('ledger_digest')!=digest_object(value,'ledger_digest'): raise IntegrityError('event ledger digest mismatch')
    prev='sha256:'+'0'*64
    for i,e in enumerate(value.get('events',[]),1):
        if e.get('sequence')!=i or e.get('previous_event_digest')!=prev or e.get('event_digest')!=digest_object(e,'event_digest'): raise IntegrityError('event chain mismatch')
        prev=e['event_digest']
    if value.get('head_digest')!=prev: raise IntegrityError('event head mismatch')
