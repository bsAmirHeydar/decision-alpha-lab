from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Mapping
from .canonical import content_hash,stable_id
from .enums import *
from .errors import ContractError,KnownTimeError,PathError

@dataclass(frozen=True)
class FeatureObservation:
    feature_ref:str; value:Any; observed_at_ms:int; source_hash:str
    def __post_init__(self):
        if not self.feature_ref or self.observed_at_ms<0 or len(self.source_hash)<8: raise ContractError('invalid feature observation')
    @property
    def feature_hash(self): return content_hash(self.semantic_payload())
    def semantic_payload(self): return {'feature_ref':self.feature_ref,'value':self.value,'observed_at_ms':self.observed_at_ms,'source_hash':self.source_hash}

@dataclass(frozen=True)
class ContextSnapshot:
    context_event_id:str; symbol:str; direction:int; decision_time_ms:int; known_as_of:str; evidence_role:str; features:tuple[FeatureObservation,...]; source_package_hash:str
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'ContextSnapshot':
        fs=tuple(FeatureObservation(str(f['feature_ref']),f['value'],int(f['observed_at_ms']),str(f['source_hash'])) for f in x['features'])
        obj=cls(str(x['context_event_id']),str(x['symbol']),int(x['direction']),int(x['decision_time_ms']),str(x['known_as_of']),str(x['evidence_role']),fs,str(x['source_package_hash']))
        if obj.direction not in (1,-1): raise ContractError('direction must be +1 or -1')
        if len({f.feature_ref for f in fs})!=len(fs): raise ContractError('duplicate feature_ref')
        future=[f.feature_ref for f in fs if f.observed_at_ms>obj.decision_time_ms]
        if future: raise KnownTimeError('future feature observations: '+','.join(sorted(future)))
        return obj
    def feature_map(self): return {f.feature_ref:f.value for f in self.features}
    def semantic_payload(self): return {'context_event_id':self.context_event_id,'symbol':self.symbol,'direction':self.direction,'decision_time_ms':self.decision_time_ms,'known_as_of':self.known_as_of,'evidence_role':self.evidence_role,'features':[f.semantic_payload() for f in sorted(self.features,key=lambda q:q.feature_ref)],'source_package_hash':self.source_package_hash}
    @property
    def snapshot_hash(self): return content_hash(self.semantic_payload())
    @property
    def snapshot_id(self): return stable_id('ctxsnap',self.semantic_payload())

@dataclass(frozen=True)
class PriceObservation:
    sequence:int; symbol:str; observed_at_ms:int; interval_open_ms:int; interval_close_ms:int; open:float; high:float; low:float; close:float; bid:float|None; ask:float|None; spread_points:float; fidelity:str; source_hash:str
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'PriceObservation':
        obj=cls(int(x['sequence']),str(x['symbol']),int(x['observed_at_ms']),int(x['interval_open_ms']),int(x['interval_close_ms']),float(x['open']),float(x['high']),float(x['low']),float(x['close']),None if x.get('bid') is None else float(x['bid']),None if x.get('ask') is None else float(x['ask']),float(x['spread_points']),str(x['fidelity']),str(x['source_hash']))
        if obj.sequence<0 or obj.low<=0 or obj.high<obj.low or not(obj.low<=obj.open<=obj.high and obj.low<=obj.close<=obj.high): raise PathError('invalid OHLC observation')
        if obj.interval_close_ms<obj.interval_open_ms or obj.observed_at_ms<obj.interval_close_ms: raise PathError('invalid observation timestamps')
        if (obj.bid is None)!=(obj.ask is None) or (obj.bid is not None and obj.ask<obj.bid): raise PathError('invalid bid/ask pair')
        if obj.spread_points<0: raise PathError('negative spread')
        return obj
    def semantic_payload(self): return self.__dict__
    @property
    def observation_hash(self): return content_hash(self.semantic_payload())
    @property
    def observation_id(self): return stable_id('priceobs',self.semantic_payload())

@dataclass(frozen=True)
class OutcomePolicy:
    policy_name:str; exact_version:str; ambiguity_policy:str; gap_policy:str; minimum_fidelity:str; maximum_observations:int; maximum_path_events_per_row:int; maximum_rows:int; strict_monotonic_sequences:bool; fail_on_symbol_mismatch:bool; require_complete_exposure:bool; require_skip_and_abstain:bool; allowed_evidence_roles:tuple[str,...]
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'OutcomePolicy':
        obj=cls(str(x['policy_name']),str(x['exact_version']),str(x['ambiguity_policy']),str(x['gap_policy']),str(x['minimum_fidelity']),int(x['maximum_observations']),int(x['maximum_path_events_per_row']),int(x['maximum_rows']),bool(x['strict_monotonic_sequences']),bool(x['fail_on_symbol_mismatch']),bool(x['require_complete_exposure']),bool(x['require_skip_and_abstain']),tuple(sorted(str(v) for v in x['allowed_evidence_roles'])))
        if min(obj.maximum_observations,obj.maximum_path_events_per_row,obj.maximum_rows)<=0: raise ContractError('policy budgets must be positive')
        return obj
    def semantic_payload(self):
        d=self.__dict__.copy();d['allowed_evidence_roles']=list(self.allowed_evidence_roles);return d
    @property
    def policy_hash(self): return content_hash(self.semantic_payload())
    @property
    def policy_id(self): return stable_id('outpolicy',self.semantic_payload())

@dataclass(frozen=True)
class CostModel:
    model_id:str; exact_version:str; spread_multiplier:float; entry_slippage_points:float; exit_slippage_points:float; commission_r:float; other_r:float
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'CostModel':
        obj=cls(str(x['model_id']),str(x['exact_version']),float(x['spread_multiplier']),float(x['entry_slippage_points']),float(x['exit_slippage_points']),float(x['commission_r']),float(x['other_r']))
        if min(obj.spread_multiplier,obj.entry_slippage_points,obj.exit_slippage_points,obj.commission_r,obj.other_r)<0: raise ContractError('negative cost input')
        return obj
    def semantic_payload(self): return self.__dict__
    @property
    def model_hash(self): return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class ExecutionSpec:
    node_id:str; node_hash:str; action_class:str; direction:int; trigger_ref:str|None; trigger_operator:str|None; trigger_expected:Any; entry_price:float|None; entry_expiration_ms:int|None; stop_price:float|None; target_price:float|None; maximum_holding_ms:int; partial_fraction:float; partial_activation_r:float; trail_activation_r:float; source_component_hashes:tuple[str,...]
    def semantic_payload(self):
        d=self.__dict__.copy();d['source_component_hashes']=list(self.source_component_hashes);return d
    @property
    def spec_hash(self):return content_hash(self.semantic_payload())
    @property
    def spec_id(self):return stable_id('execspec',self.semantic_payload())

@dataclass(frozen=True)
class PathEvent:
    sequence:int; kind:str; time_ms:int; price:float; favorable_points:float; adverse_points:float; remaining_fraction:float; event_hash:str

@dataclass(frozen=True)
class CostBreakdown:
    entry_spread_points:float; exit_spread_points:float; entry_slippage_points:float; exit_slippage_points:float; commission_r:float; other_r:float; total_cost_points:float; total_cost_r:float; cost_model_hash:str
    def semantic_payload(self):return self.__dict__
    @property
    def cost_hash(self):return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class OutcomeRow:
    node_id:str; node_hash:str; action_class:str; status:str; exit_reason:str; filled:bool; ambiguous:bool; trigger_satisfied:bool|None; entry_time_ms:int|None; entry_price:float|None; exit_time_ms:int; exit_price:float|None; stop_price:float|None; target_price:float|None; gross_points:float; gross_r:float; net_r:float; mfe_points:float; mae_points:float; mfe_r:float; mae_r:float; holding_ms:int; time_to_fill_ms:int; remaining_fraction:float; cost:CostBreakdown; path_events:tuple[PathEvent,...]; source_observation_hashes:tuple[str,...]; spec_hash:str; limitations:tuple[str,...]
    def semantic_payload(self):
        d=self.__dict__.copy();d['cost']=self.cost.semantic_payload();d['path_events']=[e.__dict__ for e in self.path_events];d['source_observation_hashes']=list(self.source_observation_hashes);d['limitations']=list(self.limitations);return d
    @property
    def row_hash(self):return content_hash(self.semantic_payload())
    @property
    def row_id(self):return stable_id('outrow',self.semantic_payload())

@dataclass(frozen=True)
class OutcomeCube:
    phase:str; version:str; cube_id:str; cube_hash:str; context_snapshot_id:str; context_snapshot_hash:str; source_lattice_id:str; source_lattice_hash:str; source_handoff_hash:str; policy_id:str; policy_hash:str; cost_registry_hash:str; evidence_role:str; known_as_of:str; decision_time_ms:int; observation_window_start_ms:int; observation_window_end_ms:int; row_count:int; ordinary_row_count:int; skip_row_count:int; abstain_row_count:int; complete_exposure:bool; selection_authority:bool; execution_authority:bool; ranking_semantics:str; rows:tuple[OutcomeRow,...]; exposure_ledger:Mapping[str,Any]; limitations:tuple[str,...]
    def semantic_payload(self):
        return {'phase':self.phase,'version':self.version,'context_snapshot_id':self.context_snapshot_id,'context_snapshot_hash':self.context_snapshot_hash,'source_lattice_id':self.source_lattice_id,'source_lattice_hash':self.source_lattice_hash,'source_handoff_hash':self.source_handoff_hash,'policy_id':self.policy_id,'policy_hash':self.policy_hash,'cost_registry_hash':self.cost_registry_hash,'evidence_role':self.evidence_role,'known_as_of':self.known_as_of,'decision_time_ms':self.decision_time_ms,'observation_window_start_ms':self.observation_window_start_ms,'observation_window_end_ms':self.observation_window_end_ms,'row_count':self.row_count,'ordinary_row_count':self.ordinary_row_count,'skip_row_count':self.skip_row_count,'abstain_row_count':self.abstain_row_count,'complete_exposure':self.complete_exposure,'selection_authority':self.selection_authority,'execution_authority':self.execution_authority,'ranking_semantics':self.ranking_semantics,'rows':[dict(r.semantic_payload(),row_id=r.row_id,row_hash=r.row_hash) for r in self.rows],'exposure_ledger':dict(self.exposure_ledger),'limitations':list(self.limitations)}
