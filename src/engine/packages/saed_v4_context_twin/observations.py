from __future__ import annotations
from collections import defaultdict
from .models import Observation,ObservableDefinition
from .canonical import parse_time
from .errors import ContractError,IdentityError

class ObservationLedger:
    def __init__(self,definitions=()):
        self.definitions={d.observable_id:d for d in definitions};self._items=[];self._ids=set()
    def append(self,obs:Observation):
        d=self.definitions.get(obs.observable_id)
        if not d:raise ContractError('unknown observable')
        if obs.observation_id in self._ids:return obs.observation_id
        if parse_time(obs.known_time)<parse_time(obs.event_time):raise ContractError('known_time before event_time')
        if not (0<=obs.quality<=1):raise ContractError('quality out of range')
        self._validate_value(d,obs.value)
        expected=1+sum(1 for x in self._items if x.twin_id==obs.twin_id)
        if obs.sequence!=expected:raise IdentityError('observation sequence gap')
        self._items.append(obs);self._ids.add(obs.observation_id);return obs.observation_id
    def _validate_value(self,d,v):
        if d.value_type=='number':
            if isinstance(v,bool) or not isinstance(v,(int,float)):raise ContractError('number required')
            if d.minimum is not None and v<d.minimum:raise ContractError('below minimum')
            if d.maximum is not None and v>d.maximum:raise ContractError('above maximum')
        elif d.value_type=='string':
            if not isinstance(v,str):raise ContractError('string required')
            if d.allowed_values and v not in d.allowed_values:raise ContractError('value not allowed')
        elif d.value_type=='boolean':
            if not isinstance(v,bool):raise ContractError('boolean required')
        else:raise ContractError('unsupported value_type')
    def visible(self,twin_id:str,known_as_of:str):
        t=parse_time(known_as_of)
        return tuple(sorted((x for x in self._items if x.twin_id==twin_id and parse_time(x.known_time)<=t),key=lambda x:(parse_time(x.known_time),x.sequence,x.observation_id)))
    def latest_by_observable(self,twin_id:str,known_as_of:str):
        out={}
        for x in self.visible(twin_id,known_as_of):out[x.observable_id]=x
        return out
