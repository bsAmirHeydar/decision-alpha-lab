from __future__ import annotations
from dataclasses import dataclass,field
from .contracts import AnatomyObservation,LifecycleRecord
from .enums import LifecycleState
class LedgerValidationError(ValueError):pass
@dataclass
class AnatomyLedger:
    observations:list[AnatomyObservation]=field(default_factory=list)
    lifecycle:list[LifecycleRecord]=field(default_factory=list)
    event_ids:list[str]=field(default_factory=list)
    def append_observation(self,o:AnatomyObservation)->None:
        o.validate(); oid=o.observation_id or o.derived_id()
        if any((x.observation_id or x.derived_id())==oid for x in self.observations):raise LedgerValidationError('duplicate observation')
        self.observations.append(o)
    def append_lifecycle(self,r:LifecycleRecord)->None:
        r.validate(); same=[x for x in self.lifecycle if x.aggregate_id==r.aggregate_id]
        if same:
            prev=same[-1]
            if r.sequence!=prev.sequence+1:raise LedgerValidationError('sequence gap')
            if r.from_state!=prev.to_state:raise LedgerValidationError('state discontinuity')
            if r.previous_record_hash!=(prev.lifecycle_id or prev.derived_id()):raise LedgerValidationError('hash discontinuity')
        elif r.sequence!=1 or r.from_state!=LifecycleState.UNKNOWN:raise LedgerValidationError('invalid first record')
        self.lifecycle.append(r)
    def append_event_id(self,event_id:str)->None:
        if event_id in self.event_ids:raise LedgerValidationError('duplicate event')
        self.event_ids.append(event_id)
    def validate(self)->None:
        for o in self.observations:o.validate()
        groups={}
        for r in self.lifecycle:groups.setdefault(r.aggregate_id,[]).append(r)
        for records in groups.values():
            records=sorted(records,key=lambda x:x.sequence)
            for i,r in enumerate(records):
                r.validate()
                if i and (r.sequence!=records[i-1].sequence+1 or r.from_state!=records[i-1].to_state):raise LedgerValidationError('broken lifecycle')
        if len(self.event_ids)!=len(set(self.event_ids)):raise LedgerValidationError('duplicate event')
