from __future__ import annotations
from datetime import datetime,timedelta,timezone
from .canonical import content_id,digest_object
from .registries import CASE_TYPES

def _iso(dt): return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')

def reference_inputs():
    base=datetime(2026,7,19,12,0,tzinfo=timezone.utc);rows=[]
    for i,case in enumerate(CASE_TYPES):
        event=base+timedelta(minutes=i*5)
        row={'schema_version':'1.0.0','case_id':f'REFCASE_{i+1:02d}_{case}','case_type':case,
             'source_identity_id':'REF_LCM04_TRACE_HARNESS_V1','environment_kind':'REFERENCE_SYNTHETIC',
             'symbol':'REFSYM','timeframe':'M15','session':'REFERENCE_SESSION','bar_index':100+i,
             'event_time':_iso(event),'available_at':_iso(event+timedelta(seconds=1)),
             'observed_at':_iso(event+timedelta(seconds=2)),'reference_fixture_only':True,
             'broker_submission_allowed':False,'input_digest':None}
        row['input_digest']=digest_object(row,'input_digest');rows.append(row)
    return rows

def build_trace(inputs):
    events=[]
    for inp in inputs:
        case=inp['case_type'];trace_id=content_id('TRACE',{'case':inp['case_id'],'input':inp['input_digest']})
        sequence=[
          ('CASE_STARTED','IDLE','CASE_ACTIVE',[]),
          ('INPUT_ACCEPTED','CASE_ACTIVE','INPUT_BOUND',['REFERENCE_FIXTURE']),
          ('DATA_AVAILABLE','INPUT_BOUND','DATA_READY',['KNOWN_TIME_SAFE']),
          ('STATE_EVALUATED','DATA_READY','EVALUATED',[f'CASE_{case}']),
        ]
        if case=='NO_TRADE': sequence.append(('NO_TRADE_EMITTED','EVALUATED','TERMINAL',['EXPLICIT_ABSTENTION']))
        elif case=='INVALIDATION': sequence.append(('INVALIDATION_EMITTED','EVALUATED','TERMINAL',['REFERENCE_INVALIDATED']))
        elif case=='EXPIRY': sequence.append(('EXPIRY_EMITTED','EVALUATED','TERMINAL',['REFERENCE_EXPIRED']))
        elif case=='DRAWING_LIFECYCLE': sequence.append(('DRAWING_INTENT_EMITTED','EVALUATED','TERMINAL',['DRAWING_CAPTURED']))
        elif case=='DRY_EXECUTION_REQUEST': sequence.append(('DRY_REQUEST_EMITTED','EVALUATED','TERMINAL',['BROKER_SUBMISSION_DISABLED']))
        elif case in {'NEGATIVE','MISSING_BAR'}: sequence.append(('NO_TRADE_EMITTED','EVALUATED','TERMINAL',['NEGATIVE_OR_INCOMPLETE']))
        else: sequence.append(('CONTEXT_EMITTED','EVALUATED','TERMINAL',['REFERENCE_EVENT']))
        sequence.append(('CASE_COMPLETED','TERMINAL','COMPLETED',['REFERENCE_FIXTURE_COMPLETE']))
        for seq,(etype,before,after,reasons) in enumerate(sequence,1):
            drawing={'object_id':'REF_LCM04_OBJECT','anchor_time':inp['event_time'],'anchor_price':'100.00000','action':'CREATE_THEN_DELETE'} if etype=='DRAWING_INTENT_EMITTED' else None
            dry={'action':'BUY_LIMIT','symbol':'REFSYM','volume':'0.00','price':'100.00000','submission_enabled':False} if etype=='DRY_REQUEST_EMITTED' else None
            e={'schema_version':'1.0.0','trace_id':trace_id,'case_id':inp['case_id'],'case_type':case,
               'sequence':seq,'source_identity_id':inp['source_identity_id'],'environment_kind':inp['environment_kind'],
               'event_type':etype,'event_time':inp['event_time'],'available_at':inp['available_at'],'observed_at':inp['observed_at'],
               'symbol':inp['symbol'],'timeframe':inp['timeframe'],'session':inp['session'],'bar_index':inp['bar_index'],
               'bar_status':'MISSING' if case=='MISSING_BAR' else ('CURRENT_OPEN' if case=='CURRENT_BAR_INTRABAR' else 'CLOSED'),
               'state_before':before,'state_after':after,'context_event':'REFERENCE_CONTEXT' if etype=='CONTEXT_EMITTED' else None,
               'setup_event':None,'treatment_event':None,'reason_codes':reasons,'drawing_spec':drawing,
               'dry_execution_request':dry,'broker_submission_performed':False,'source_behavior_modified':False,
               'evidence_status':'REFERENCE_FIXTURE_ONLY','event_digest':None}
            e['event_digest']=digest_object(e,'event_digest');events.append(e)
    return events

def trace_bundle(events):
    by={}
    for e in events: by.setdefault(e['trace_id'],[]).append(e)
    traces=[]
    for tid,rows in sorted(by.items()):
        rows=sorted(rows,key=lambda x:x['sequence'])
        tr={'trace_id':tid,'case_id':rows[0]['case_id'],'case_type':rows[0]['case_type'],'event_count':len(rows),
            'event_digests':[x['event_digest'] for x in rows],'trace_digest':None}
        tr['trace_digest']=digest_object(tr,'trace_digest');traces.append(tr)
    obj={'schema_version':'1.0.0','phase_id':'LCM-04','evidence_status':'REFERENCE_FIXTURE_ONLY',
         'trace_count':len(traces),'event_count':len(events),'traces':traces,'bundle_digest':None}
    obj['bundle_digest']=digest_object(obj,'bundle_digest');return obj
