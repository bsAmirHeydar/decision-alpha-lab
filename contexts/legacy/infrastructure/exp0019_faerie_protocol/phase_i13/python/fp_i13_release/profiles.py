from dataclasses import replace
from .contracts import *
from .canonical import sha256

def _p(pid,days,objects,ops,chunk,alerts,export,mode,diag=True):
    p=ReleaseProfile(pid,days,objects,ops,chunk,alerts,export,mode,diag,'')
    return replace(p,profile_hash=p.computed_hash)
PROFILES=(
 _p(ReleaseProfileId.TRADING_30D,30,2500,200,256,True,False,'STANDARD'),
 _p(ReleaseProfileId.AUDIT_90D,90,5000,400,512,False,True,'AUDIT'),
 _p(ReleaseProfileId.PERFORMANCE_7D,7,1000,100,128,False,False,'MINIMAL'),
 _p(ReleaseProfileId.SAFE_DIAGNOSTIC,14,1500,150,128,False,True,'AUDIT'),
)
def get_profile(profile_id):
    if isinstance(profile_id,str): profile_id=ReleaseProfileId(profile_id)
    return next(x for x in PROFILES if x.profile_id==profile_id)
