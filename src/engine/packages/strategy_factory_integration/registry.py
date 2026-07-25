from __future__ import annotations
from dataclasses import dataclass
from .enums import LifecycleState
from .hashing import stable_id
from .models import CanonicalAnatomyEvent, LifecycleRecord

class EventDedupRegistry:
    def __init__(self, capacity: int = 4096):
        if capacity < 1: raise ValueError("capacity must be positive")
        self.capacity=capacity; self._seen: dict[str,int]={}
    def register(self, event: CanonicalAnatomyEvent, now_ms: int) -> bool:
        if event.event_id in self._seen:
            self._seen[event.event_id]=now_ms; return False
        if len(self._seen)>=self.capacity: raise OverflowError("dedup registry capacity")
        self._seen[event.event_id]=now_ms; return True
    def __len__(self): return len(self._seen)

class LifecycleLedger:
    def __init__(self, capacity: int = 8192):
        if capacity < 1: raise ValueError("capacity must be positive")
        self.capacity=capacity; self._first: dict[str,int]={}; self._last: dict[str,int]={}; self._records:list[LifecycleRecord]=[]
    @property
    def records(self)->tuple[LifecycleRecord,...]: return tuple(self._records)
    def observe(self, event_id: str, now_ms: int, pulse_sequence: int) -> LifecycleRecord:
        first=self._first.get(event_id,now_ms); self._first.setdefault(event_id,now_ms); self._last[event_id]=now_ms
        state=LifecycleState.FIRST_SEEN if first==now_ms and not any(r.event_id==event_id for r in self._records) else LifecycleState.ACTIVE
        return self._append(event_id,state,first,now_ms,pulse_sequence,"candidate_present")
    def retire_missing(self, active_ids:set[str], now_ms:int, pulse_sequence:int)->tuple[LifecycleRecord,...]:
        out=[]
        for event_id,last in list(self._last.items()):
            if event_id in active_ids: continue
            out.append(self._append(event_id,LifecycleState.RETIRED,self._first[event_id],now_ms,pulse_sequence,"candidate_absent_on_completed_pulse"))
            del self._last[event_id]
        return tuple(out)
    def _append(self,event_id,state,first,last,pulse,reason):
        if len(self._records)>=self.capacity: raise OverflowError("lifecycle ledger capacity")
        rec=LifecycleRecord(stable_id("sf20life",f"{event_id}|{state.value}|{first}|{last}|{pulse}"),event_id,state,first,last,pulse,reason)
        self._records.append(rec); return rec
