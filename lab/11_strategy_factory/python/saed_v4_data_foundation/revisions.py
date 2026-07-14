from __future__ import annotations
from collections import defaultdict
from .models import SovereignRecord
from .canonical import parse_time
from .errors import ImmutableConflict,TemporalIntegrityError
class RevisionStore:
    def __init__(self): self._by_entity=defaultdict(list); self._by_id={}
    def append(self,record:SovereignRecord)->str:
        rid=record.revision_id
        if rid in self._by_id:
            if self._by_id[rid]!=record: raise ImmutableConflict('revision id conflict')
            return rid
        chain=self._by_entity[record.entity_id]
        if record.revision_number!=len(chain)+1: raise TemporalIntegrityError('revision_number must extend chain by one')
        expected=chain[-1].revision_id if chain else None
        if record.supersedes_revision_id!=expected: raise TemporalIntegrityError('supersedes_revision_id must point to current head')
        if chain and parse_time(record.temporal.known_time)<parse_time(chain[-1].temporal.known_time): raise TemporalIntegrityError('known_time cannot move backward in a revision chain')
        chain.append(record); self._by_id[rid]=record; return rid
    def latest(self,entity_id:str)->SovereignRecord: return self._by_entity[entity_id][-1]
    def as_of(self,entity_id:str,known_as_of:str,event_as_of:str|None=None)->SovereignRecord|None:
        visible=[r for r in self._by_entity.get(entity_id,[]) if r.temporal.visible_as_of(known_as_of,event_as_of)]
        return visible[-1] if visible else None
    def records_as_of(self,known_as_of:str,event_as_of:str|None=None)->tuple[SovereignRecord,...]:
        out=[]
        for entity in sorted(self._by_entity):
            r=self.as_of(entity,known_as_of,event_as_of)
            if r is not None: out.append(r)
        return tuple(out)
