from __future__ import annotations
from .canonical import digest_object,content_id
from .errors import IntegrityError

def build(identity_run_id: str, issued_at: str, payloads: list[tuple[str,dict]]):
    events=[]; prev=None
    for seq,(etype,payload) in enumerate(payloads,1):
        e={'sequence':seq,'event_id':content_id('LCM03EVT',{'run':identity_run_id,'sequence':seq,'type':etype},24),'event_type':etype,'occurred_at':issued_at,'previous_event_digest':prev,'payload':payload,'source_move_authority':False,'source_delete_authority':False,'semantic_refactor_authority':False,'runtime_authority':False,'live_order_authority':False,'capital_authority':False,'event_digest':None}
        e['event_digest']=digest_object(e,'event_digest');prev=e['event_digest'];events.append(e)
    out={'schema_version':'1.0.0','phase_id':'LCM-03','identity_run_id':identity_run_id,'event_count':len(events),'events':events,'ledger_digest':None};out['ledger_digest']=digest_object(out,'ledger_digest');return out

def verify(ledger: dict):
    prev=None
    for i,e in enumerate(ledger.get('events',[]),1):
        if e['sequence']!=i or e['previous_event_digest']!=prev or e['event_digest']!=digest_object(e,'event_digest'): raise IntegrityError('LCM-03 event chain mismatch')
        prev=e['event_digest']
    if ledger.get('event_count')!=len(ledger.get('events',[])) or ledger.get('ledger_digest')!=digest_object(ledger,'ledger_digest'): raise IntegrityError('LCM-03 ledger mismatch')
    return True
