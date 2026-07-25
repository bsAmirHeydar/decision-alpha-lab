from __future__ import annotations
from .canonical import digest_object,stable_id,with_digest
def build_event_ledger(run_id:str,at:str,payloads:list[tuple[str,dict]])->dict:
    events=[]; prev='GENESIS'
    for i,(typ,payload) in enumerate(payloads,1):
        body={'schema_version':'1.0.0','event_id':stable_id('ACLEVT',run_id,str(i),typ),'sequence':i,'event_type':typ,'occurred_at':at,'previous_event_digest':prev,'payload':payload,'pilot_execution_authority':False,'runtime_generation_authority':False,'live_order_authority':False,'capital_authority':False}
        event=with_digest(body,'event_digest'); events.append(event); prev=event['event_digest']
    return with_digest({'schema_version':'1.0.0','fleet_closure_run_id':run_id,'event_count':len(events),'events':events},'ledger_digest')
def verify_event_ledger(doc:dict)->bool:
    from .canonical import verify_embedded_digest
    if not verify_embedded_digest(doc,'ledger_digest'): return False
    prev='GENESIS'
    for i,e in enumerate(doc.get('events',[]),1):
        if e.get('sequence')!=i or e.get('previous_event_digest')!=prev or not verify_embedded_digest(e,'event_digest'): return False
        if any(e.get(k) for k in ['pilot_execution_authority','runtime_generation_authority','live_order_authority','capital_authority']): return False
        prev=e['event_digest']
    return doc.get('event_count')==len(doc.get('events',[]))
