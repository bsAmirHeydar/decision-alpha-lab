from .canonical import content_id,digest_object
def build(run_id,payloads):
    prev=None;events=[]
    for i,(typ,payload) in enumerate(payloads,1):
        e={"schema_version":"1.0.0","event_id":content_id('LCM05EV',[run_id,i,typ,payload]),"sequence":i,"event_type":typ,"occurred_at":"2026-07-19T00:00:00Z","previous_event_digest":prev,"payload":payload,"source_move_authority":False,"source_delete_authority":False,"target_materialization_authority":False,"runtime_authority":False,"live_order_authority":False,"capital_authority":False,"event_digest":None};e['event_digest']=digest_object(e,'event_digest');prev=e['event_digest'];events.append(e)
    obj={"schema_version":"1.0.0","topology_run_id":run_id,"event_count":len(events),"events":events,"final_event_digest":prev,"ledger_digest":None};obj['ledger_digest']=digest_object(obj,'ledger_digest');return obj
