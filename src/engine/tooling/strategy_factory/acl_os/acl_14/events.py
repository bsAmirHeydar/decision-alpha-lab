from __future__ import annotations
from .canonical import digest_object,stable_id,with_digest
def build_event_ledger(run_id:str,occurred_at:str,items:list[tuple[str,dict]])->dict:
    events=[]; prev='GENESIS'
    for i,(typ,payload) in enumerate(items,1):
        body={'schema_version':'1.0.0','event_id':stable_id('ACL14EVT',run_id,str(i),typ,length=28),'sequence':i,'event_type':typ,'occurred_at':occurred_at,'previous_event_digest':prev,'payload':payload,'pilot_execution_authority':False,'runtime_activation_authority':False,'live_order_authority':False,'capital_authority':False}
        evt=with_digest(body,'event_digest'); events.append(evt); prev=evt['event_digest']
    return with_digest({'schema_version':'1.0.0','pilot_run_id':run_id,'event_count':len(events),'events':events,'final_event_digest':prev},'ledger_digest')
def verify_event_ledger(doc:dict)->bool:
    prev='GENESIS'
    for i,e in enumerate(doc.get('events',[]),1):
        if e.get('sequence')!=i or e.get('previous_event_digest')!=prev: return False
        if e.get('event_digest')!=digest_object({k:v for k,v in e.items() if k!='event_digest'}): return False
        prev=e['event_digest']
    return doc.get('event_count')==len(doc.get('events',[])) and doc.get('final_event_digest')==prev and doc.get('ledger_digest')==digest_object({k:v for k,v in doc.items() if k!='ledger_digest'})
