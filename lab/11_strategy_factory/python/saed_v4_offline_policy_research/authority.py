from __future__ import annotations
from .errors import AuthorityError
DENIALS={'decision':False,'execution':False,'production':False,'promotion':False,'risk_allocation':False,'runtime':False,'order_submission':False,'online_learning':False,'live_policy_update':False}
def authority_boundary(): return {'phase':'SAED_V4_23','research_only':True,'offline_only':True,'authority':dict(DENIALS),'fallbacks':['skip','abstain','manual_baseline','reject','quarantine']}
def assert_no_authority(x):
    if any(bool(v) for v in x.get('authority',{}).values()): raise AuthorityError('authority escalation')
    return True
