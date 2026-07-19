from __future__ import annotations
from .canonical import digest_object,content_id

def build(run_id,payloads,occurred_at):
    prev=None;events=[]
    for i,(etype,payload) in enumerate(payloads,1):
        e={'sequence':i,'event_id':content_id('LCM04EVENT',{'r':run_id,'s':i,'t':etype}),
           'event_type':etype,'occurred_at':occurred_at,'previous_event_digest':prev,'payload':payload,
           'source_move_authority':False,'source_delete_authority':False,'semantic_refactor_authority':False,
           'runtime_authority':False,'live_order_authority':False,'capital_authority':False,'event_digest':None}
        e['event_digest']=digest_object(e,'event_digest');prev=e['event_digest'];events.append(e)
    obj={'schema_version':'1.0.0','phase_id':'LCM-04','characterization_run_id':run_id,'event_count':len(events),
         'events':events,'ledger_digest':None};obj['ledger_digest']=digest_object(obj,'ledger_digest');return obj

def verify(obj):
    prev=None
    for i,e in enumerate(obj['events'],1):
        if e['sequence']!=i or e['previous_event_digest']!=prev or e['event_digest']!=digest_object(e,'event_digest'): raise ValueError('event chain invalid')
        prev=e['event_digest']
    if obj['ledger_digest']!=digest_object(obj,'ledger_digest'): raise ValueError('ledger digest invalid')
    return True
