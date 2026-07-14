from __future__ import annotations
from dataclasses import dataclass
from .canonical import normalize_time,parse_time
from .errors import TemporalIntegrityError
@dataclass(frozen=True)
class BitemporalStamp:
    event_time:str
    known_time:str
    valid_to:str|None=None
    def __post_init__(self):
        e=parse_time(self.event_time); k=parse_time(self.known_time)
        if k<e: raise TemporalIntegrityError('known_time cannot precede event_time')
        if self.valid_to is not None and parse_time(self.valid_to)<=e: raise TemporalIntegrityError('valid_to must follow event_time')
        object.__setattr__(self,'event_time',normalize_time(self.event_time)); object.__setattr__(self,'known_time',normalize_time(self.known_time))
        if self.valid_to is not None: object.__setattr__(self,'valid_to',normalize_time(self.valid_to))
    def visible_as_of(self,known_as_of:str,event_as_of:str|None=None)->bool:
        if parse_time(self.known_time)>parse_time(known_as_of): return False
        if event_as_of is None: return True
        t=parse_time(event_as_of)
        return parse_time(self.event_time)<=t and (self.valid_to is None or t<parse_time(self.valid_to))
