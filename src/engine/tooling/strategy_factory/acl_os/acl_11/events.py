from __future__ import annotations
from .canonical import digest_object,stable_id
def build_event_ledger(run_id: str,at: str,events: list[tuple[str,dict]]) -> dict:
    prev='GENESIS'; out=[]
    for seq,(typ,payload) in enumerate(events,1):
        body={'schema_version':'1.0.0','event_id':stable_id('RTEVT',run_id,str(seq),typ),'sequence':seq,'event_type':typ,'occurred_at':at,'previous_event_digest':prev,'payload':payload,'runtime_generation_authority':False,'runtime_activation_authority':False,'live_order_authority':False,'capital_authority':False}
        event={**body,'event_digest':digest_object(body)}; out.append(event); prev=event['event_digest']
    body={'schema_version':'1.0.0','runtime_custody_run_id':run_id,'event_count':len(out),'events':out,'terminal_event_digest':prev}
    return {**body,'ledger_digest':digest_object(body)}
def verify_event_ledger(l: dict) -> bool:
    prev='GENESIS'
    for i,e in enumerate(l.get('events',[]),1):
        if e.get('sequence')!=i or e.get('previous_event_digest')!=prev: return False
        if e.get('event_digest')!=digest_object({k:v for k,v in e.items() if k!='event_digest'}): return False
        prev=e['event_digest']
    return l.get('terminal_event_digest')==prev and l.get('ledger_digest')==digest_object({k:v for k,v in l.items() if k!='ledger_digest'})
