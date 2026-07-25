from __future__ import annotations
from dataclasses import replace
from .events import make_event,verify_chain
from .enums import *
from .errors import FPI09Error

class AppendOnlyLedger:
    def __init__(self): self._events=[]; self._signal_hashes={}; self._event_ids=set()
    @property
    def events(self): return tuple(self._events)
    @property
    def chain_head_hash(self): return self._events[-1].event_hash if self._events else ""
    def append(self,event):
        if event.event_id in self._event_ids: return False
        if event.sequence!=len(self._events): raise FPI09Error("FP_LDG_EVENT_SEQUENCE_GAP","event sequence must append exactly")
        expected=self.chain_head_hash
        if event.prior_event_hash!=expected: raise FPI09Error("FP_LDG_EVENT_CHAIN_BREAK","prior event hash mismatch")
        self._events.append(event); self._event_ids.add(event.event_id)
        if not verify_chain(self._events): self._events.pop(); self._event_ids.remove(event.event_id); raise FPI09Error("FP_LDG_EVENT_HASH_INVALID","event hash invalid")
        return True
    def ingest_signal(self,signal,occurred_utc_ms):
        known=self._signal_hashes.get(signal.signal_id)
        if known:
            typ=LedgerEventType.DUPLICATE_SIGNAL_IGNORED if known==signal.signal_hash else LedgerEventType.SIGNAL_COLLISION_BLOCKED
            reason="FP_LDG_DUPLICATE_SIGNAL_IGNORED" if known==signal.signal_hash else "FP_LDG_SIGNAL_ID_COLLISION"
            e=make_event(len(self._events),typ,signal.signal_id,occurred_utc_ms,{"signal_id":signal.signal_id,"signal_hash":signal.signal_hash},signal_id=signal.signal_id,reason_code=reason,prior_event_hash=self.chain_head_hash)
            self.append(e)
            if typ is LedgerEventType.SIGNAL_COLLISION_BLOCKED: raise FPI09Error("FP_LDG_SIGNAL_ID_COLLISION","same signal id with different semantic hash")
            return e,False
        self._signal_hashes[signal.signal_id]=signal.signal_hash
        e=make_event(len(self._events),LedgerEventType.SIGNAL_INGESTED,signal.signal_id,occurred_utc_ms,{"signal_id":signal.signal_id,"signal_hash":signal.signal_hash},signal_id=signal.signal_id,reason_code="FP_LDG_SIGNAL_INGESTED",prior_event_hash=self.chain_head_hash)
        self.append(e); return e,True
    def append_fact(self,event_type,aggregate_id,occurred_utc_ms,payload,**kw):
        e=make_event(len(self._events),event_type,aggregate_id,occurred_utc_ms,payload,prior_event_hash=self.chain_head_hash,**kw); self.append(e); return e
