from __future__ import annotations
from collections import deque
from .enums import OverflowPolicy
from .models import TelemetryEvent

class TelemetryRing:
    def __init__(self, capacity: int, overflow_policy: OverflowPolicy=OverflowPolicy.DROP_OLDEST):
        if capacity<1: raise ValueError("capacity must be positive")
        self.capacity=capacity; self.overflow_policy=overflow_policy
        self._items: deque[TelemetryEvent]=deque()
        self._event_ids:set[str]=set(); self._last_sequence:dict[str,int]={}
        self.dropped_count=0; self.duplicate_count=0; self.rejected_sequence_count=0
    def append(self,event:TelemetryEvent)->bool:
        if event.event_id in self._event_ids:
            self.duplicate_count+=1; return False
        last=self._last_sequence.get(event.run_id,0)
        if event.sequence<=last:
            self.rejected_sequence_count+=1; return False
        if len(self._items)>=self.capacity:
            if self.overflow_policy==OverflowPolicy.REJECT_NEW:
                self.dropped_count+=1; return False
            old=self._items.popleft(); self._event_ids.remove(old.event_id); self.dropped_count+=1
        self._items.append(event); self._event_ids.add(event.event_id); self._last_sequence[event.run_id]=event.sequence
        return True
    def snapshot(self)->tuple[TelemetryEvent,...]: return tuple(self._items)
    def __len__(self)->int: return len(self._items)
