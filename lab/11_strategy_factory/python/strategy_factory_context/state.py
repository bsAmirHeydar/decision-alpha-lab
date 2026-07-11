from __future__ import annotations
from dataclasses import dataclass
from strategy_factory_contracts.records import FeatureValue
from strategy_factory_contracts.time import MarketTimestamp
@dataclass(slots=True)
class ContextEntry:
    value:FeatureValue; computed_generation:int; expires_at_ms:int; dirty:bool=False; invalidation_reason:str='NONE'
class ContextState:
    def __init__(self,capacity:int=256):
        if not 1<=capacity<=4096:raise ValueError('invalid context capacity')
        self.capacity=capacity;self.entries={};self.generation=0;self.event_id='';self.snapshot_time=MarketTimestamp(0)
    def begin_generation(self,generation:int,event_id:str,snapshot_time:MarketTimestamp)->None:
        if generation<0:raise ValueError('negative generation')
        self.generation=generation;self.event_id=event_id;self.snapshot_time=snapshot_time
    def put(self,value:FeatureValue,max_age_ms:int)->None:
        if value.known_time>self.snapshot_time:raise ValueError('future feature')
        if value.feature_id not in self.entries and len(self.entries)>=self.capacity:raise ValueError('context capacity exceeded')
        expires=self.snapshot_time.utc_epoch_milliseconds if max_age_ms<=0 else value.known_time.utc_epoch_milliseconds+max_age_ms
        self.entries[value.feature_id]=ContextEntry(value,self.generation,expires)
    def get(self,feature_id:str)->FeatureValue|None:
        entry=self.entries.get(feature_id);return None if entry is None else entry.value
    def mark_all_dirty(self,reason:str='EVENT')->None:
        for entry in self.entries.values():entry.dirty=True;entry.invalidation_reason=reason
    def mark_dirty(self,feature_id:str,reason:str='DEPENDENCY')->bool:
        entry=self.entries.get(feature_id)
        if entry is None:return False
        entry.dirty=True;entry.invalidation_reason=reason;return True
    def is_dirty(self,feature_id:str)->bool:
        entry=self.entries.get(feature_id);return entry is None or entry.dirty
    def is_fresh(self,feature_id:str,at_ms:int)->bool:
        entry=self.entries.get(feature_id);return bool(entry and not entry.dirty and at_ms<=entry.expires_at_ms)
