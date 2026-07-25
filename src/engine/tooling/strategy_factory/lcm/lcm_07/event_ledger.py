from .canonical import content_id,digest_object

def build(run_id,payloads):
    prev=None;events=[]
    for i,(typ,payload) in enumerate(payloads,1):
        e={"schema_version":"1.0.0","event_id":content_id("LCM07EV",[run_id,i,typ,payload]),"sequence":i,"event_type":typ,"occurred_at":"2026-07-19T00:00:00Z","previous_event_digest":prev,"payload":payload,"source_move_authority":False,"source_delete_authority":False,"target_materialization_authority":False,"semantic_refactor_authority":False,"merge_authority":False,"runtime_authority":False,"live_order_authority":False,"capital_authority":False,"event_digest":None};e["event_digest"]=digest_object(e,"event_digest");prev=e["event_digest"];events.append(e)
    o={"schema_version":"1.0.0","shared_engine_run_id":run_id,"event_count":len(events),"events":events,"final_event_digest":prev,"ledger_digest":None};o["ledger_digest"]=digest_object(o,"ledger_digest");return o
