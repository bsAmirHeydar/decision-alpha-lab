from __future__ import annotations
from .models import QuarantineRecord
from .errors import ImmutableConflict,QuarantineRequired
class QuarantineRegistry:
    def __init__(self): self._items={}
    def add(self,item:QuarantineRecord):
        if item.quarantine_id in self._items and self._items[item.quarantine_id]!=item: raise ImmutableConflict('quarantine record conflict')
        self._items[item.quarantine_id]=item; return item.quarantine_id
    def is_blocked(self,subject_id:str)->bool: return any(x.subject_id==subject_id and not x.resolved for x in self._items.values())
    def require_clear(self,subject_id:str):
        if self.is_blocked(subject_id): raise QuarantineRequired(subject_id)
    def resolve(self,quarantine_id:str,resolution_hash:str):
        old=self._items[quarantine_id]
        if old.resolved:
            if old.resolution_hash!=resolution_hash: raise ImmutableConflict('resolved quarantine is immutable')
            return old
        new=QuarantineRecord(old.quarantine_id,old.subject_id,old.reason,old.details,old.evidence_hash,True,resolution_hash); self._items[quarantine_id]=new; return new
