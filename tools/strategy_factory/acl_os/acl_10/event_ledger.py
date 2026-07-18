from __future__ import annotations
from typing import Any
from .canonical import stable_id, with_digest, digest_object

def build_event_ledger(promotion_run_id:str, events:list[tuple[str,dict[str,Any]]], at:str) -> dict[str,Any]:
    rows=[]; previous='GENESIS'
    for sequence,(event_type,payload) in enumerate(events,1):
        body={'schema_version':'1.0.0','event_id':stable_id('PROEVT',promotion_run_id,str(sequence),event_type),'sequence':sequence,'event_type':event_type,'occurred_at':at,'previous_event_digest':previous,'payload':payload,'promotion_execution_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        row=with_digest(body,'event_digest'); rows.append(row); previous=row['event_digest']
    return with_digest({'schema_version':'1.0.0','promotion_run_id':promotion_run_id,'event_count':len(rows),'events':rows,'terminal_event_digest':previous},'ledger_digest')
def verify_event_ledger(document:dict[str,Any]) -> bool:
    if document.get('ledger_digest') != digest_object({k:v for k,v in document.items() if k!='ledger_digest'}): return False
    rows=document.get('events',[]); previous='GENESIS'
    if document.get('event_count') != len(rows): return False
    for sequence,row in enumerate(rows,1):
        if row.get('sequence')!=sequence or row.get('previous_event_digest')!=previous: return False
        if row.get('event_digest') != digest_object({k:v for k,v in row.items() if k!='event_digest'}): return False
        if any([row.get('promotion_execution_allowed'),row.get('runtime_generation_allowed'),row.get('live_order_submission_allowed'),row.get('capital_activation_allowed')]): return False
        previous=row['event_digest']
    return previous==document.get('terminal_event_digest')
