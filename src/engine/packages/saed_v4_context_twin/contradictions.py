from __future__ import annotations
from .models import Contradiction
from .enums import ContradictionSeverity
from .errors import ContradictionError

class ContradictionRegistry:
    def __init__(self):self._items={}
    def open(self,item:Contradiction):
        old=self._items.get(item.contradiction_id)
        if old and old!=item:raise ContradictionError('contradiction rebind')
        self._items[item.contradiction_id]=item;return item.contradiction_id
    def resolve(self,contradiction_id:str,resolution_hash:str):
        old=self._items.get(contradiction_id)
        if not old:raise ContradictionError('unknown contradiction')
        if len(resolution_hash)!=64:raise ContradictionError('resolution hash required')
        self._items[contradiction_id]=Contradiction(old.twin_id,old.contradiction_key,old.left_hash,old.right_hash,old.severity,old.known_time,old.description,True,resolution_hash)
    def active(self,twin_id:str):return tuple(sorted((x for x in self._items.values() if x.twin_id==twin_id and not x.resolved),key=lambda x:x.contradiction_id))
    def blocking(self,twin_id:str):return tuple(x for x in self.active(twin_id) if x.severity in {ContradictionSeverity.MATERIAL,ContradictionSeverity.CRITICAL})
    def all(self,twin_id:str):return tuple(sorted((x for x in self._items.values() if x.twin_id==twin_id),key=lambda x:x.contradiction_id))
