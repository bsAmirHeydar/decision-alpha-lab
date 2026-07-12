"""Causal observation lifecycle with duplicate suppression and transition evidence."""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Mapping, Any
from strategy_factory_contracts_v3 import IdentityKind, KnownTimeChain, UtcInstant, build_identity, canonical_sha256
from .enums import ContextLifecycleState
from .errors import LifecycleError
from .utils import safe_id, contract_safe

_TERMINAL={ContextLifecycleState.INVALIDATED,ContextLifecycleState.EXPIRED,ContextLifecycleState.SUPERSEDED,ContextLifecycleState.RETIRED}
_ALLOWED={
 ContextLifecycleState.DETECTED:{ContextLifecycleState.CONFIRMED,ContextLifecycleState.INVALIDATED,ContextLifecycleState.EXPIRED,ContextLifecycleState.SUPERSEDED,ContextLifecycleState.RETIRED},
 ContextLifecycleState.CONFIRMED:{ContextLifecycleState.ACTIVE,ContextLifecycleState.INVALIDATED,ContextLifecycleState.EXPIRED,ContextLifecycleState.SUPERSEDED,ContextLifecycleState.RETIRED},
 ContextLifecycleState.ACTIVE:{ContextLifecycleState.INVALIDATED,ContextLifecycleState.EXPIRED,ContextLifecycleState.SUPERSEDED,ContextLifecycleState.RETIRED},
 ContextLifecycleState.INVALIDATED:{ContextLifecycleState.RETIRED}, ContextLifecycleState.EXPIRED:{ContextLifecycleState.RETIRED}, ContextLifecycleState.SUPERSEDED:{ContextLifecycleState.RETIRED}, ContextLifecycleState.RETIRED:set(),
}

@dataclass(frozen=True, slots=True)
class ContextObservation:
    package_id: str; package_version: str; source_event_ids: tuple[str,...]; symbol_scope: tuple[str,...]; timeframe_scope_seconds: tuple[int,...]
    lifecycle_state: ContextLifecycleState; time_chain: KnownTimeChain; payload: Mapping[str,Any]; parent_observation_id: str="none"; supersedes_observation_id: str="none"; sequence: int=0
    def __post_init__(self) -> None:
        safe_id(self.package_id,"package_id"); safe_id(self.package_version,"package_version"); safe_id(self.parent_observation_id,"parent_observation_id"); safe_id(self.supersedes_observation_id,"supersedes_observation_id")
        if not self.source_event_ids: raise LifecycleError("observation_without_source","context observation requires at least one source event")
        if not self.symbol_scope: raise LifecycleError("observation_without_symbol","context observation requires symbol scope")
        if any(x<=0 for x in self.timeframe_scope_seconds): raise LifecycleError("invalid_timeframe","timeframes must be positive")
        if self.sequence < 0: raise LifecycleError("negative_sequence","sequence may not be negative")
    def identity_material(self) -> Mapping[str,Any]:
        return {"event_time_ms":self.time_chain.event_time.epoch_ms,"package_id":self.package_id,"package_version":self.package_version,"parent_observation_id":self.parent_observation_id,"source_event_ids":sorted(self.source_event_ids),"symbol_scope":sorted(self.symbol_scope),"timeframe_scope_seconds":sorted(self.timeframe_scope_seconds)}
    @property
    def observation_id(self) -> str:
        return build_identity(IdentityKind.CONTEXT_OCCURRENCE,namespace="ucee.context_observation",version=self.package_version,owner_id=self.package_id,**self.identity_material()).stable_id
    def material(self) -> Mapping[str,Any]:
        return {"lifecycle_state":self.lifecycle_state.value,"observation_id":self.observation_id,"package_id":self.package_id,"package_version":self.package_version,"parent_observation_id":self.parent_observation_id,"payload":contract_safe(self.payload),"sequence":self.sequence,"source_event_ids":list(self.source_event_ids),"supersedes_observation_id":self.supersedes_observation_id,"symbol_scope":list(self.symbol_scope),"time_chain":self.time_chain.material(),"timeframe_scope_seconds":list(self.timeframe_scope_seconds)}
    @property
    def observation_hash(self) -> str: return canonical_sha256(self.material())

@dataclass(frozen=True, slots=True)
class ObservationTransition:
    transition_id: str; observation_id: str; from_state: ContextLifecycleState; to_state: ContextLifecycleState; known_time: UtcInstant; reason_code: str; evidence_hash: str; sequence: int

class ContextLifecycleEngine:
    def __init__(self, capacity: int=4096) -> None:
        if capacity<1: raise LifecycleError("invalid_capacity","capacity must be positive")
        self.capacity=capacity; self._records: dict[str,ContextObservation]={}; self._transitions: list[ObservationTransition]=[]; self.duplicates_suppressed=0
    def register(self, observation: ContextObservation) -> tuple[ContextObservation,bool]:
        oid=observation.observation_id
        existing=self._records.get(oid)
        if existing is not None:
            if existing.observation_hash != observation.observation_hash: raise LifecycleError("identity_collision","same observation identity has different canonical payload",{"observation_id":oid})
            self.duplicates_suppressed+=1; return existing,False
        if len(self._records)>=self.capacity: raise LifecycleError("lifecycle_capacity_exceeded","lifecycle registry is full",{"capacity":self.capacity})
        self._records[oid]=observation; return observation,True
    def transition(self, observation_id: str, to_state: ContextLifecycleState, known_time: UtcInstant, reason_code: str, evidence: Mapping[str,Any] | None=None) -> ContextObservation:
        safe_id(reason_code,"reason_code")
        current=self._records.get(observation_id)
        if current is None: raise LifecycleError("unknown_observation","observation is not registered",{"observation_id":observation_id})
        if to_state == current.lifecycle_state: return current
        if to_state not in _ALLOWED[current.lifecycle_state]: raise LifecycleError("illegal_transition","lifecycle transition is not allowed",{"from":current.lifecycle_state.value,"to":to_state.value})
        if known_time.epoch_ms < current.time_chain.known_time.epoch_ms: raise LifecycleError("transition_time_reversal","transition known_time precedes observation known_time")
        sequence=current.sequence+1
        updated=replace(current,lifecycle_state=to_state,sequence=sequence)
        material={"evidence":contract_safe(evidence or {}),"from":current.lifecycle_state.value,"known_time_ms":known_time.epoch_ms,"observation_id":observation_id,"reason_code":reason_code,"sequence":sequence,"to":to_state.value}
        tid=build_identity(IdentityKind.EVIDENCE_BUNDLE,namespace="ucee.context_transition",version=current.package_version,owner_id=current.package_id,**material).stable_id
        self._transitions.append(ObservationTransition(tid,observation_id,current.lifecycle_state,to_state,known_time,reason_code,canonical_sha256(material),sequence))
        self._records[observation_id]=updated; return updated
    def supersede(self, old_observation_id: str, replacement: ContextObservation, known_time: UtcInstant, reason_code: str="newer_context_occurrence") -> tuple[ContextObservation,ContextObservation]:
        if replacement.supersedes_observation_id not in ("none",old_observation_id): raise LifecycleError("supersession_link_mismatch","replacement points to a different observation")
        replacement=replace(replacement,supersedes_observation_id=old_observation_id)
        new,_=self.register(replacement)
        old=self.transition(old_observation_id,ContextLifecycleState.SUPERSEDED,known_time,reason_code,{"replacement_observation_id":new.observation_id})
        return old,new
    def get(self, observation_id: str) -> ContextObservation | None: return self._records.get(observation_id)
    @property
    def records(self) -> tuple[ContextObservation,...]: return tuple(self._records[k] for k in sorted(self._records))
    @property
    def transitions(self) -> tuple[ObservationTransition,...]: return tuple(self._transitions)
