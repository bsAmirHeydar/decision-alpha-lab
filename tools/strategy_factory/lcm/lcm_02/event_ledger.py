from __future__ import annotations
from .canonical import content_id,digest_object
from .errors import IntegrityError

def build(classification_id: str, payloads: list[tuple[str,dict]], occurred_at: str):
    prev=None; events=[]
    for i,(kind,payload) in enumerate(payloads,1):
        e={'schema_version':'1.0.0','sequence':i,'event_id':content_id('LCM02EVT',[classification_id,i,kind]),'event_type':kind,'occurred_at':occurred_at,'previous_event_digest':prev,'payload':payload,'move_authority':False,'delete_authority':False,'semantic_refactor_authority':False,'runtime_authority':False,'live_order_authority':False,'capital_authority':False}
        e['event_digest']=digest_object(e,'event_digest'); prev=e['event_digest']; events.append(e)
    ledger={'schema_version':'1.0.0','classification_id':classification_id,'events':events,'event_count':len(events),'terminal_event_digest':prev}
    ledger['ledger_digest']=digest_object(ledger,'ledger_digest'); return ledger
def verify(ledger):
    prev=None
    for i,e in enumerate(ledger.get('events',[]),1):
        if e.get('sequence')!=i or e.get('previous_event_digest')!=prev or e.get('event_digest')!=digest_object(e,'event_digest'): raise IntegrityError('LCM-02 event chain mismatch')
        if any(e.get(k) for k in ['move_authority','delete_authority','semantic_refactor_authority','runtime_authority','live_order_authority','capital_authority']): raise IntegrityError('event authority escalation')
        prev=e['event_digest']
    if ledger.get('terminal_event_digest')!=prev or ledger.get('ledger_digest')!=digest_object(ledger,'ledger_digest'): raise IntegrityError('LCM-02 ledger digest mismatch')
    return True
