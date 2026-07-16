from __future__ import annotations
from .errors import AuthorityError
DENIALS={'decision':False,'execution':False,'promotion':False,'production':False,'risk_allocation':False,'runtime':False,'order_submission':False,'positive_alpha_evidence':False}
def authority_boundary(): return {'phase':'SAED_V4_22','research_only':True,'synthetic_stress_only':True,'authority':dict(DENIALS),'fallbacks':['skip','abstain','manual','reject','quarantine']}
def assert_no_authority(x):
    if any(bool(v) for v in x.get('authority',{}).values()): raise AuthorityError('authority escalation')
    return True
