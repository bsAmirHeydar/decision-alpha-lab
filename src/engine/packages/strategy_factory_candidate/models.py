from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping
from .enums import *
from .hashing import stable_id, cdouble

@dataclass(frozen=True, slots=True)
class PolicyParameters:
    numeric: tuple[float,...]=(0.0,)*8
    integers: tuple[int,...]=(0,)*8
    text: str=""
    def canonical(self)->str:
        if len(self.numeric)!=8 or len(self.integers)!=8: raise ValueError("policy parameter vectors must have length 8")
        return "".join(f"|d{i}={cdouble(v)}" for i,v in enumerate(self.numeric))+"".join(f"|i{i}={int(v)}" for i,v in enumerate(self.integers))+f"|s={self.text}"
    @property
    def hash(self)->str:return stable_id("ppar",self.canonical())

@dataclass(frozen=True, slots=True)
class PolicyDescriptor:
    policy_id:str; version:str; kind:PolicyKind; deterministic:bool=True; fast_path_safe:bool=True; replay_safe:bool=True
    requires_reference_price:bool=False; requires_invalidation_price:bool=False; required_feature_ids:tuple[str,...]=(); description:str=""
    def canonical(self)->str:
        return "|".join([self.policy_id,self.version,str(int(self.kind)),str(self.deterministic).lower(),str(self.fast_path_safe).lower(),str(self.replay_safe).lower(),str(self.requires_reference_price).lower(),str(self.requires_invalidation_price).lower(),",".join(self.required_feature_ids),self.description])
    @property
    def hash(self)->str:return stable_id("pdesc",self.canonical())

@dataclass(frozen=True, slots=True)
class CandidateTemplate:
    template_id:str; template_version:str; enabled:bool; priority:int
    entry_policy_id:str; entry_policy_version:str; entry_parameters:PolicyParameters
    stop_policy_id:str; stop_policy_version:str; stop_parameters:PolicyParameters
    exit_policy_id:str; exit_policy_version:str; exit_parameters:PolicyParameters
    admissibility_tag:str=""
    def canonical(self)->str:
        return "|".join([self.template_id,self.template_version,str(self.enabled).lower(),str(self.priority),self.entry_policy_id,self.entry_policy_version,self.entry_parameters.hash,self.stop_policy_id,self.stop_policy_version,self.stop_parameters.hash,self.exit_policy_id,self.exit_policy_version,self.exit_parameters.hash,self.admissibility_tag])
    @property
    def hash(self)->str:return stable_id("ctpl",self.canonical())

@dataclass(frozen=True, slots=True)
class AnatomyEvent:
    event_id:str; strategy_id:str; strategy_version:str; symbol:str; direction:int; reference_price:float; invalidation_price:float; known_time_ms:int; confirmation_time_ms:int; source_hash:str
@dataclass(frozen=True, slots=True)
class FeatureSnapshot:
    snapshot_id:str; event_id:str; state_generation:int; snapshot_time_ms:int; values:Mapping[str,float]
@dataclass(frozen=True, slots=True)
class ContextFrame:
    frame_id:str; event_id:str; snapshot_id:str; state_generation:int
@dataclass(frozen=True, slots=True)
class EntryPlan:
    order_kind:OrderKind; requested_price:float; activation_time_ms:int; expiration_time_ms:int; max_fill_delay_ms:int=0; max_slippage_points:float=0.0
    def canonical(self):return "|".join(map(str,[int(self.order_kind),cdouble(self.requested_price),self.activation_time_ms,self.expiration_time_ms,self.max_fill_delay_ms,cdouble(self.max_slippage_points)]))
@dataclass(frozen=True, slots=True)
class StopPlan:
    stop_price:float; initial_risk_points:float; has_price_stop:bool=True; has_time_invalidation:bool=False; invalidation_time_ms:int=0
    def canonical(self):return "|".join(map(str,[str(self.has_price_stop).lower(),cdouble(self.stop_price),str(self.has_time_invalidation).lower(),self.invalidation_time_ms,cdouble(self.initial_risk_points)]))
@dataclass(frozen=True, slots=True)
class ExitPlan:
    exit_kind:ExitKind; target_price:float; planned_reward_points:float; has_price_target:bool=True; max_holding_ms:int=0; partial_fraction:float=0.0
    def canonical(self):return "|".join(map(str,[int(self.exit_kind),str(self.has_price_target).lower(),cdouble(self.target_price),self.max_holding_ms,cdouble(self.planned_reward_points),cdouble(self.partial_fraction)]))
@dataclass(frozen=True, slots=True)
class TradeCandidate:
    template_id:str; template_hash:str; event_id:str; snapshot_id:str; context_frame_id:str; strategy_id:str; strategy_version:str; symbol:str; direction:int; runtime_generation_id:int; created_at_ms:int; entry:EntryPlan; stop:StopPlan; exit_plan:ExitPlan; source_hash:str; status:CandidateStatus=CandidateStatus.VALID
    @property
    def planned_r_multiple(self)->float:return self.exit_plan.planned_reward_points/self.stop.initial_risk_points
    def canonical(self)->str:
        return "|".join(["alpha_lab.strategy_factory/trade_candidate@1.0.0",self.template_id,self.template_hash,self.event_id,self.snapshot_id,self.context_frame_id,self.strategy_id,self.strategy_version,self.symbol,str(self.direction),str(self.runtime_generation_id),str(self.created_at_ms),stable_id("epln",self.entry.canonical()),stable_id("spln",self.stop.canonical()),stable_id("xpln",self.exit_plan.canonical()),cdouble(self.planned_r_multiple),self.source_hash])
    @property
    def candidate_id(self)->str:return stable_id("cand",self.canonical())
