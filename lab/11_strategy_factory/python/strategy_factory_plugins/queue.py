from collections import deque
from dataclasses import dataclass
from enum import Enum
from .enums import QueueOverflowPolicy
class QueueResult(str,Enum): INSERTED="INSERTED";DUPLICATE="DUPLICATE";REJECTED_FULL="REJECTED_FULL";DROPPED_OLDEST="DROPPED_OLDEST";FAILED="FAILED"
@dataclass(frozen=True,slots=True)
class QueueTelemetry: inserted:int;popped:int;duplicates:int;overflows:int;depth:int;capacity:int;failed:bool
class AnatomyEventQueue:
    def __init__(self,capacity,overflow_policy,duplicate_window=None):
        if not 1<=capacity<=65536: raise ValueError("capacity")
        self.capacity=capacity;self.policy=overflow_policy;self.window=duplicate_window if duplicate_window is not None else capacity*4
        self.items=deque();self.recent=deque(maxlen=self.window or None);self.recent_set=set();self.inserted=self.popped=self.duplicates=self.overflows=0;self.failed=False
    def _remember(self,i):
        if self.window==0:return
        if len(self.recent)==self.recent.maxlen and self.recent:self.recent_set.discard(self.recent[0])
        self.recent.append(i);self.recent_set.add(i)
    def push(self,i,v):
        if self.failed:return QueueResult.FAILED
        if i in self.recent_set:self.duplicates+=1;return QueueResult.DUPLICATE
        result=QueueResult.INSERTED
        if len(self.items)>=self.capacity:
            self.overflows+=1
            if self.policy is QueueOverflowPolicy.REJECT_NEW:return QueueResult.REJECTED_FULL
            if self.policy is QueueOverflowPolicy.FAIL_PLUGIN:self.failed=True;return QueueResult.FAILED
            self.items.popleft();result=QueueResult.DROPPED_OLDEST
        self.items.append(v);self._remember(i);self.inserted+=1;return result
    def pop(self):
        if not self.items:return None
        self.popped+=1;return self.items.popleft()
    @property
    def telemetry(self):return QueueTelemetry(self.inserted,self.popped,self.duplicates,self.overflows,len(self.items),self.capacity,self.failed)
