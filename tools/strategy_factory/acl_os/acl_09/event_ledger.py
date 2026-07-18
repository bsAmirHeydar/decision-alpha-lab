from __future__ import annotations
from typing import Any
from .canonical import stable_id,with_digest,digest_object
def build_event_ledger(memory_run_id:str,events:list[tuple[str,dict[str,Any]]],at:str)->dict[str,Any]:
    rows=[]; prev='GENESIS'
    for i,(kind,payload) in enumerate(events,1):
        body={'schema_version':'1.0.0','event_id':stable_id('MEMEVT',memory_run_id,str(i),kind),'sequence':i,'event_type':kind,'occurred_at':at,'previous_event_digest':prev,'payload':payload,'research_execution_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        row=with_digest(body,'event_digest'); rows.append(row); prev=row['event_digest']
    return with_digest({'schema_version':'1.0.0','memory_run_id':memory_run_id,'event_count':len(rows),'events':rows,'terminal_event_digest':prev},'ledger_digest')
def verify_event_ledger(doc:dict[str,Any])->bool:
    if doc.get('ledger_digest')!=digest_object({k:v for k,v in doc.items() if k!='ledger_digest'}): return False
    rows=doc.get('events',[])
    if doc.get('event_count')!=len(rows): return False
    prev='GENESIS'
    for i,row in enumerate(rows,1):
        if row.get('sequence')!=i or row.get('previous_event_digest')!=prev: return False
        if row.get('event_digest')!=digest_object({k:v for k,v in row.items() if k!='event_digest'}): return False
        if 'research_execution_allowed' in row and row.get('research_execution_allowed') is not False: return False
        if row.get('live_order_submission_allowed') is not False or row.get('capital_activation_allowed') is not False: return False
        prev=row['event_digest']
    return doc.get('terminal_event_digest')==prev
