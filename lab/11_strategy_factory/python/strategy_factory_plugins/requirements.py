from dataclasses import dataclass
from strategy_factory_contracts.hashing import stable_id
from strategy_factory_contracts.validation import validate_safe_identifier,validate_terminal_symbol
from .enums import RequirementKind,RequirementStrength
@dataclass(frozen=True,slots=True)
class DataRequirement:
    requirement_id:str;kind:RequirementKind;strength:RequirementStrength;symbol:str;timeframe_seconds:int=0;lookback_bars:int=0;max_staleness_msc:int=0;max_close_skew_msc:int=0;synchronization_group_id:str="";purpose:str=""
    def __post_init__(self):
        validate_safe_identifier(self.requirement_id,"requirement_id");validate_terminal_symbol(self.symbol)
        if self.kind is RequirementKind.CLOSED_BARS and (self.timeframe_seconds<=0 or not 2<=self.lookback_bars<=100000): raise ValueError("closed bars need timeframe and lookback")
        if self.timeframe_seconds<0 or self.lookback_bars<0 or self.max_staleness_msc<0 or self.max_close_skew_msc<0: raise ValueError("negative requirement value")
        if self.synchronization_group_id: validate_safe_identifier(self.synchronization_group_id,"synchronization_group_id")
    @property
    def canonical_payload(self): return "|".join([self.requirement_id,self.kind.value,self.strength.value,self.symbol,str(self.timeframe_seconds),str(self.lookback_bars),str(self.max_staleness_msc),str(self.max_close_skew_msc),self.synchronization_group_id])
@dataclass(frozen=True,slots=True)
class PluginRequirements:
    items:tuple[DataRequirement,...]
    def __post_init__(self):
        ids=[x.requirement_id for x in self.items]
        if len(ids)!=len(set(ids)): raise ValueError("duplicate requirement")
    @property
    def canonical_payload(self): return "||".join(x.canonical_payload for x in self.items)
    @property
    def requirements_hash(self): return stable_id("req",self.canonical_payload)
