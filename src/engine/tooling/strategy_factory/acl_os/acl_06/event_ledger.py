from __future__ import annotations
from .canonical import digest_object,stable_id,with_digest
class EventLedger:
    def __init__(self,run_id:str): self.run_id=run_id; self.events=[]
    def append(self,event_type:str,payload:dict,occurred_at:str):
        prev=self.events[-1]['event_digest'] if self.events else None; seq=len(self.events)+1
        body={'schema_version':'1.0.0','event_id':stable_id('ACLEVT',self.run_id,str(seq),event_type,length=24),'run_id':self.run_id,'sequence':seq,'event_type':event_type,'occurred_at':occurred_at,'previous_event_digest':prev,'payload':payload,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        self.events.append({**body,'event_digest':digest_object(body)})
    def document(self): return with_digest({'schema_version':'1.0.0','run_id':self.run_id,'events':self.events,'event_count':len(self.events)},'ledger_digest')
def verify_event_ledger(doc:dict)->bool:
    prev=None
    for i,e in enumerate(doc.get('events',[]),1):
        if e.get('sequence')!=i or e.get('previous_event_digest')!=prev: return False
        body={k:v for k,v in e.items() if k!='event_digest'}
        if e.get('event_digest')!=digest_object(body): return False
        prev=e['event_digest']
    return doc.get('event_count')==len(doc.get('events',[])) and doc.get('ledger_digest')==digest_object({k:v for k,v in doc.items() if k!='ledger_digest'})
