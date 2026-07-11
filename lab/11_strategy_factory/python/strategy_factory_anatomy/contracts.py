from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from strategy_factory_contracts.hashing import stable_id
from .enums import ObservationKind, LifecycleState, ALLOWED

def _safe(v:str)->bool: return bool(v) and all(c.isalnum() or c in '._-:#' for c in v)
@dataclass(frozen=True,slots=True)
class AnatomyObservation:
    plugin_id:str; plugin_version:str; symbol:str; timeframe_seconds:int; kind:ObservationKind
    occurred_at_ms:int; known_at_ms:int; reference_price:float; extreme_price:float; close_price:float
    source_bar_id:str; source_hash:str; market_event_cluster_id:str; observation_id:str=''
    schema:str='alpha_lab.strategy_factory/anatomy_observation@1.0.0'
    def canonical(self)->str:
        return '|'.join([self.schema,self.plugin_id,self.plugin_version,self.symbol,str(self.timeframe_seconds),str(int(self.kind)),str(self.occurred_at_ms),str(self.known_at_ms),format(self.reference_price,'.17g'),format(self.extreme_price,'.17g'),format(self.close_price,'.17g'),self.source_bar_id,self.source_hash,self.market_event_cluster_id])
    def derived_id(self)->str:return stable_id('obs',self.canonical())
    def validate(self)->None:
        if self.schema!='alpha_lab.strategy_factory/anatomy_observation@1.0.0':raise ValueError('schema')
        if not _safe(self.plugin_id) or not _safe(self.plugin_version):raise ValueError('plugin identity')
        if not self.symbol or self.timeframe_seconds<=0 or self.kind==ObservationKind.UNKNOWN:raise ValueError('shape')
        if self.occurred_at_ms<0 or self.known_at_ms<self.occurred_at_ms:raise ValueError('time')
        if not all(_safe(x) for x in (self.source_bar_id,self.source_hash,self.market_event_cluster_id)):raise ValueError('lineage')
        if self.observation_id and self.observation_id!=self.derived_id():raise ValueError('id')
@dataclass(frozen=True,slots=True)
class LifecycleRecord:
    aggregate_id:str; sequence:int; from_state:LifecycleState; to_state:LifecycleState; transition_time_ms:int; reason_code:str; source_hash:str; previous_record_hash:str='none'; lifecycle_id:str=''; schema:str='alpha_lab.strategy_factory/anatomy_lifecycle@1.0.0'
    def canonical(self)->str:return '|'.join([self.schema,self.aggregate_id,str(self.sequence),str(int(self.from_state)),str(int(self.to_state)),str(self.transition_time_ms),self.reason_code,self.source_hash,self.previous_record_hash])
    def derived_id(self)->str:return stable_id('life',self.canonical())
    def validate(self)->None:
        if (self.from_state,self.to_state) not in ALLOWED:raise ValueError('transition')
        if self.sequence<1 or not _safe(self.aggregate_id) or not _safe(self.reason_code) or not _safe(self.source_hash):raise ValueError('fields')
        if self.sequence>1 and not _safe(self.previous_record_hash):raise ValueError('chain')
        if self.lifecycle_id and self.lifecycle_id!=self.derived_id():raise ValueError('id')
@dataclass(frozen=True,slots=True)
class GoldenLedgerManifest:
    case_id:str; plugin_id:str; plugin_version:str; input_fixture_hash:str; expected_observation_ids:tuple[str,...]; expected_event_ids:tuple[str,...]; expected_record_count:int; schema:str='alpha_lab.strategy_factory/golden_ledger_manifest@1.0.0'
    def validate(self)->None:
        if not all(_safe(x) for x in (self.case_id,self.plugin_id,self.plugin_version,self.input_fixture_hash)):raise ValueError('identity')
        if self.expected_record_count<0:raise ValueError('count')
        if len(set(self.expected_observation_ids))!=len(self.expected_observation_ids):raise ValueError('duplicate observations')
        if len(set(self.expected_event_ids))!=len(self.expected_event_ids):raise ValueError('duplicate events')
