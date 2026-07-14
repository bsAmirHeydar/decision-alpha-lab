from .contracts import *
from .canonical import *
from .constants import ZERO_HASH
from .errors import FPI15Error
class ReconciliationLedger:
    def __init__(self,events=()):
        self.events=[]; self.ids={}
        for e in events: self.append_existing(e)
    def append(self,event_type,aggregate_id,event_utc_ms,payload,reason_codes=()):
        payload_hash=sha256(payload); eid=stable_id("FPEVT",{"type":event_type,"aggregate":aggregate_id,"payload":payload_hash})
        if eid in self.ids:
            if self.ids[eid]!=payload_hash: raise FPI15Error("FP_PAPER_EVENT_ID_COLLISION","same event id different payload")
            return self.events[[e.event_id for e in self.events].index(eid)],False
        prior=self.events[-1].event_hash if self.events else ZERO_HASH
        seq=len(self.events)+1
        eh=sha256({"sequence":seq,"type":event_type,"aggregate":aggregate_id,"time":event_utc_ms,"payload":payload_hash,"prior":prior,"event_id":eid,"reasons":tuple(sorted(set(reason_codes)))})
        ev=ReconciliationEvent(seq,event_type,aggregate_id,event_utc_ms,payload_hash,prior,eid,eh,tuple(sorted(set(reason_codes))))
        self.events.append(ev); self.ids[eid]=payload_hash; return ev,True
    def append_existing(self,e):
        expected_prior=self.events[-1].event_hash if self.events else ZERO_HASH
        if e.sequence!=len(self.events)+1 or e.prior_event_hash!=expected_prior: raise FPI15Error("FP_PAPER_LEDGER_CHAIN_INVALID","ledger chain invalid")
        if e.event_id in self.ids and self.ids[e.event_id]!=e.payload_hash: raise FPI15Error("FP_PAPER_EVENT_ID_COLLISION","checkpoint collision")
        self.events.append(e); self.ids[e.event_id]=e.payload_hash
    @property
    def chain_head(self): return self.events[-1].event_hash if self.events else ZERO_HASH
