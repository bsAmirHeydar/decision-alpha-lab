from .models import *
from .enums import *

def reference_bundle(now: int = 2_000_000):
    release=MicroLiveRelease("sf18.reference.release","1.0.0","sf.reference","1.0.0",18,"model_release",
        "decision_policy","risk_policy","allocation_policy","execution_policy",123456,"Broker-Demo",("X",),0.01,1,
        now-1000,now+60000,"soak_evidence","reconciliation_evidence","anti_overfit_evidence")
    release=MicroLiveRelease(**{**release.__dict__,"release_hash":release.derived_hash()})
    auth=LiveAuthorization("auth.reference",release.release_hash,123456,"Broker-Demo","X",LiveMode.DRY_RUN,
        now-1000,now+30000,0.01,1,"nonce-001","operator-token")
    auth=LiveAuthorization(**{**auth.__dict__,"authorization_hash":auth.derived_hash()})
    policy=LiveSafetyPolicy("sf18.reference.safety","1.0.0",1,1,1,0.01,0.01,100,200,250,1000,500,100,50,1000,1000,5,2,5000,True,True,True,False)
    policy=LiveSafetyPolicy(**{**policy.__dict__,"policy_hash":policy.derived_hash()})
    intent=ExecutionIntentRecord("intent-1","intent-hash","batch-1","candidate-1","candidate-hash","context-1",
        "sf.reference","1.0.0","X","group-1",1,18,"model_release","decision_policy","risk_policy","allocation_policy",
        OrderKind.MARKET,100,99,102,True,0.01,100,80,now-100,now+10000,True)
    account=AccountGuardSnapshot(123456,"Broker-Demo",10000,10000,9000,1000,0,0,0,0,0,True,True,True,now)
    account=AccountGuardSnapshot(**{**account.__dict__,"snapshot_hash":account.derived_hash()})
    quote=QuoteSnapshot("X",100,100.1,0.01,now,1)
    return release,auth,policy,intent,account,quote
