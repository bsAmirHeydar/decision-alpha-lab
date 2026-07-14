from .contracts import *
from .canonical import sha256,stable_id

def compare_runs(left:ReplayRun,right:ReplayRun)->ParityReport:
    fields=('semantic_payloads','visual_semantic_ids','alert_ids','suppressed_historical_alert_ids','export_ids','health_codes','event_chain_hash','last_sequence','inventory_hash')
    mismatches=[]
    for f in fields:
        if getattr(left.inventory,f)!=getattr(right.inventory,f): mismatches.append(f)
    status=ParityStatus.PASS if not mismatches else ParityStatus.FAIL
    body={'left':left.run_id,'right':right.run_id,'status':status.value,'fields':fields,'mismatches':tuple(mismatches)}
    return ParityReport(stable_id('FPPARITY',body),left.run_id,right.run_id,status,fields,tuple(mismatches),sha256(body))
