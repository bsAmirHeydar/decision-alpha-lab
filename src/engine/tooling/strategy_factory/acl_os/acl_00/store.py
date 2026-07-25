from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
from .errors import ConcurrencyError
from .types import LifecycleState

@dataclass(frozen=True,slots=True)
class SubjectState:
    subject_id:str
    tenant_id:str
    state:LifecycleState
    revision:int

class InMemoryStateStore:
    def __init__(self): self._items={}; self._lock=RLock()
    def seed(self,item:SubjectState)->None:
        with self._lock: self._items[item.subject_id]=item
    def get(self,subject_id:str)->SubjectState|None:
        with self._lock: return self._items.get(subject_id)
    def compare_and_set(self,subject_id:str,tenant_id:str,expected_revision:int,from_state:LifecycleState,to_state:LifecycleState)->SubjectState:
        with self._lock:
            current=self._items.get(subject_id)
            if current is None:
                if expected_revision!=0 or from_state!=LifecycleState.DRAFT_CONTEXT: raise ConcurrencyError("subject not seeded and request is not initial revision")
                current=SubjectState(subject_id,tenant_id,from_state,0)
            if current.tenant_id!=tenant_id: raise ConcurrencyError("tenant mismatch")
            if current.revision!=expected_revision: raise ConcurrencyError("revision mismatch")
            if current.state!=from_state: raise ConcurrencyError("from_state mismatch")
            nxt=SubjectState(subject_id,tenant_id,to_state,current.revision+1); self._items[subject_id]=nxt; return nxt
