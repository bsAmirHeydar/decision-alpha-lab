from .contracts import LifecycleEvent
from .canonical import canonical_sha256,stable_id
from .enums import LifecycleEventType

class LifecycleEventChain:
    def __init__(self,instance_id): self.instance_id=instance_id; self.events=[]
    @property
    def head(self): return self.events[-1].event_hash if self.events else '0'*64
    def append(self,event_type:LifecycleEventType,occurred_utc_ms:int,reason_code:str,payload):
        seq=len(self.events); prior='' if seq==0 else self.events[-1].event_hash; payload_hash=canonical_sha256(payload)
        material={'sequence':seq,'event_type':event_type.value,'occurred_utc_ms':occurred_utc_ms,'instance_id':self.instance_id,'reason_code':reason_code,'payload_hash':payload_hash,'prior_event_hash':prior}
        event_hash=canonical_sha256(material); event=LifecycleEvent(stable_id('FPEVT',material),seq,event_type,occurred_utc_ms,self.instance_id,reason_code,payload_hash,prior,event_hash); self.events.append(event); return event
    def validate(self):
        prior=''
        for i,e in enumerate(self.events):
            if e.sequence!=i or e.prior_event_hash!=prior: return False
            material={'sequence':e.sequence,'event_type':e.event_type.value,'occurred_utc_ms':e.occurred_utc_ms,'instance_id':e.instance_id,'reason_code':e.reason_code,'payload_hash':e.payload_hash,'prior_event_hash':e.prior_event_hash}
            if canonical_sha256(material)!=e.event_hash: return False
            prior=e.event_hash
        return True
