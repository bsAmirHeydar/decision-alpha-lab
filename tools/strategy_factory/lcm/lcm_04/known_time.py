from __future__ import annotations
from datetime import datetime
from .canonical import digest_object

def _dt(v): return datetime.fromisoformat(v.replace('Z','+00:00'))

def audit(events):
    findings=[]
    for e in events:
        ok=_dt(e['event_time'])<=_dt(e['available_at'])<=_dt(e['observed_at'])
        if not ok: findings.append({'trace_id':e['trace_id'],'sequence':e['sequence'],'reason_code':'KNOWN_TIME_ORDER_VIOLATION'})
    obj={'schema_version':'1.0.0','phase_id':'LCM-04','event_count':len(events),'finding_count':len(findings),
         'status':'PASS' if not findings else 'FAIL','future_data_detected':bool(findings),'findings':findings,
         'audit_digest':None};obj['audit_digest']=digest_object(obj,'audit_digest');return obj
