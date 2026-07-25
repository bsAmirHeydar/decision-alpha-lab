from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping
from .enums import EntryOrderType,SizingUnit
from .utils import stable_id,canonical_value
@dataclass(frozen=True,slots=True)
class EntryLeg:
    order_type:EntryOrderType; trigger_price:Decimal; allocation_fraction:Decimal; earliest_time_ms:int; latest_time_ms:int; limit_price:Decimal|None=None
    def to_dict(self): return {'order_type':self.order_type.value,'trigger_price':self.trigger_price,'limit_price':self.limit_price,'allocation_fraction':self.allocation_fraction,'earliest_time_ms':self.earliest_time_ms,'latest_time_ms':self.latest_time_ms}
@dataclass(frozen=True,slots=True)
class EntryPlan:
    invocation_id:str; legs:tuple[EntryLeg,...]; cancel_policy:str='cancel_on_context_invalidation'; metadata:Mapping[str,str]|None=None
    @property
    def plan_id(self): return stable_id('uceep',self.to_dict())
    def to_dict(self): return {'invocation_id':self.invocation_id,'legs':[x.to_dict() for x in self.legs],'cancel_policy':self.cancel_policy,'metadata':canonical_value(self.metadata or {})}
@dataclass(frozen=True,slots=True)
class StopPlan:
    invocation_id:str; stop_price:Decimal|None; distance:Decimal|None; time_exit_ms:int|None=None; catastrophic_price:Decimal|None=None; metadata:Mapping[str,str]|None=None
    @property
    def plan_id(self): return stable_id('ucesp',self.to_dict())
    def to_dict(self): return {'invocation_id':self.invocation_id,'stop_price':self.stop_price,'distance':self.distance,'time_exit_ms':self.time_exit_ms,'catastrophic_price':self.catastrophic_price,'metadata':canonical_value(self.metadata or {})}
@dataclass(frozen=True,slots=True)
class TargetLeg:
    target_price:Decimal|None; quantity_fraction:Decimal; activation_r:Decimal|None=None; is_runner:bool=False
    def to_dict(self): return {'target_price':self.target_price,'quantity_fraction':self.quantity_fraction,'activation_r':self.activation_r,'is_runner':self.is_runner}
@dataclass(frozen=True,slots=True)
class TargetPlan:
    invocation_id:str; legs:tuple[TargetLeg,...]; no_fixed_target:bool=False; metadata:Mapping[str,str]|None=None
    @property
    def plan_id(self): return stable_id('ucetp',self.to_dict())
    def to_dict(self): return {'invocation_id':self.invocation_id,'legs':[x.to_dict() for x in self.legs],'no_fixed_target':self.no_fixed_target,'metadata':canonical_value(self.metadata or {})}
@dataclass(frozen=True,slots=True)
class TrailingPlan:
    invocation_id:str; mode:str; activation_r:Decimal; distance:Decimal|None; lock_r:Decimal|None; cadence_ms:int; reference_field:str=''; metadata:Mapping[str,str]|None=None
    @property
    def plan_id(self): return stable_id('ucetrp',self.to_dict())
    def to_dict(self): return {'invocation_id':self.invocation_id,'mode':self.mode,'activation_r':self.activation_r,'distance':self.distance,'lock_r':self.lock_r,'cadence_ms':self.cadence_ms,'reference_field':self.reference_field,'metadata':canonical_value(self.metadata or {})}
@dataclass(frozen=True,slots=True)
class ManagementRule:
    rule_type:str; activation_value:Decimal|int|str; quantity_fraction:Decimal; action_value:Decimal|int|str|None=None
    def to_dict(self): return {'rule_type':self.rule_type,'activation_value':self.activation_value,'quantity_fraction':self.quantity_fraction,'action_value':self.action_value}
@dataclass(frozen=True,slots=True)
class ManagementPlan:
    invocation_id:str; rules:tuple[ManagementRule,...]; metadata:Mapping[str,str]|None=None
    @property
    def plan_id(self): return stable_id('ucemp',self.to_dict())
    def to_dict(self): return {'invocation_id':self.invocation_id,'rules':[x.to_dict() for x in self.rules],'metadata':canonical_value(self.metadata or {})}
@dataclass(frozen=True,slots=True)
class SizingPlan:
    invocation_id:str; unit:SizingUnit; requested_value:Decimal; cap_value:Decimal|None; scale_factor:Decimal=Decimal('1'); metadata:Mapping[str,str]|None=None
    @property
    def plan_id(self): return stable_id('ucezp',self.to_dict())
    def to_dict(self): return {'invocation_id':self.invocation_id,'unit':self.unit.value,'requested_value':self.requested_value,'cap_value':self.cap_value,'scale_factor':self.scale_factor,'metadata':canonical_value(self.metadata or {})}
