from __future__ import annotations
from .models import SourceValue
from .errors import SourceConflictError,TemporalBoundaryError
from .canonical import parse_time
from .temporal import validate_boundary
class SourceFrame:
    def __init__(self,values=()):
        self._items={}
        for value in values:self.add(value)
    def add(self,value:SourceValue):
        if not (0.0<=value.quality<=1.0):raise SourceConflictError('quality outside [0,1]')
        if len(value.source_hash)!=64:raise SourceConflictError('invalid source hash')
        key=value.source_key;old=self._items.get(key)
        if old and (old.value_hash!=value.value_hash or old.source_hash!=value.source_hash or old.known_time!=value.known_time):raise SourceConflictError('conflicting source value: '+key)
        self._items[key]=value;return value
    def get(self,namespace,path):return self._items.get(f'{namespace}:{path}')
    def visible(self,namespace,path,known_as_of,event_as_of,evidence_role):
        value=self.get(namespace,path)
        if value is None:return None
        if value.evidence_role!=evidence_role:raise TemporalBoundaryError('evidence role mismatch')
        try:validate_boundary(value.event_time,value.known_time,known_as_of,event_as_of)
        except ValueError as exc:raise TemporalBoundaryError(str(exc))
        return value
    def all(self):return tuple(self._items[k] for k in sorted(self._items))
