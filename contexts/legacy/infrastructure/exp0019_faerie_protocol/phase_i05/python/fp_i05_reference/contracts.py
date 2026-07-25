from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
import math
from typing import Mapping
from fp_i02_kernel.enums import WindowKind, PriceSide, ReferenceState, LookbackPolicy, ReferenceReusePolicy
from fp_i04_data.contracts import M1Bar
from .canonical import canonical_sha256, stable_id, require_identifier, require_semver, require_sha256
from .constants import *
from .enums import *
from .errors import FPI05Error

def _req(v,n):
    if not isinstance(v,str) or not v.strip(): raise FPI05Error('FP_RRC_REQUIRED_FIELD',f'{n} is required',{'field':n})
    return v

def _minute(v,n):
    if not isinstance(v,int) or v<0 or v%M1_MS: raise FPI05Error('FP_RRC_MINUTE_INVALID',f'{n} must be aligned UTC M1')
    return v

def _finite(v,n):
    if not isinstance(v,(int,float)) or not math.isfinite(float(v)): raise FPI05Error('FP_RRC_NONFINITE_VALUE',f'{n} must be finite')
    return float(v)

@dataclass(frozen=True,slots=True)
class WindowStoreConfig:
    context_id:str
    pair_id:str
    calendar_config_hash:str
    data_contract_registry_hash:str
    calendar_day_depth:int=DEFAULT_CALENDAR_DAY_DEPTH
    minimum_coverage_ratio:float=DEFAULT_MINIMUM_COVERAGE_RATIO
    lookback_policy:LookbackPolicy=LookbackPolicy.CALENDAR_DAY_DEPTH
    reference_reuse_policy:ReferenceReusePolicy=ReferenceReusePolicy.ALLOW_UNTIL_PROTECTED_TOUCH
    require_completed_reference_windows:bool=True
    version:str=WINDOW_STORE_VERSION
    def __post_init__(self):
        require_identifier(self.context_id,'context_id');require_identifier(self.pair_id,'pair_id')
        require_sha256(self.calendar_config_hash,'calendar_config_hash');require_sha256(self.data_contract_registry_hash,'data_contract_registry_hash');require_semver(self.version,'version')
        if self.calendar_day_depth<1 or self.calendar_day_depth>366: raise FPI05Error('FP_RRC_DEPTH_INVALID','calendar day depth outside [1,366]')
        if not 0 < float(self.minimum_coverage_ratio) <= 1: raise FPI05Error('FP_RRC_COVERAGE_THRESHOLD_INVALID','minimum coverage ratio must be (0,1]')
        if self.lookback_policy is not LookbackPolicy.CALENDAR_DAY_DEPTH: raise FPI05Error('FP_RRC_LOOKBACK_POLICY_INVALID','only calendar-day depth is canonical')
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class WindowDescriptor:
    descriptor_id:str
    pair_id:str
    kind:WindowKind
    trading_date:str
    trading_day_id:str
    week_id:str
    start_utc_ms:int
    end_utc_ms:int
    expected_minutes:int
    calendar_config_hash:str
    source_calendar_window_id:str
    version:str=WINDOW_STORE_VERSION
    def __post_init__(self):
        _req(self.descriptor_id,'descriptor_id');require_identifier(self.pair_id,'pair_id');_req(self.trading_date,'trading_date');_req(self.trading_day_id,'trading_day_id')
        _minute(self.start_utc_ms,'start_utc_ms');_minute(self.end_utc_ms,'end_utc_ms')
        if self.end_utc_ms<=self.start_utc_ms or self.expected_minutes<1: raise FPI05Error('FP_RRC_WINDOW_INTERVAL_INVALID','window interval invalid')
        require_sha256(self.calendar_config_hash,'calendar_config_hash');_req(self.source_calendar_window_id,'source_calendar_window_id');require_semver(self.version,'version')
        if self.kind is WindowKind.W and not self.week_id: raise FPI05Error('FP_RRC_WEEK_ID_REQUIRED','W window requires week_id')
    @property
    def descriptor_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class SymbolWindowAggregate:
    aggregate_id:str
    descriptor_id:str
    canonical_symbol:str
    state:WindowBuildState
    open:float|None
    high:float|None
    low:float|None
    close:float|None
    high_utc_ms:int|None
    low_utc_ms:int|None
    present_minutes:int
    expected_elapsed_minutes:int
    expected_total_minutes:int
    missing_minutes:int
    out_of_coverage_minutes:int
    conflict_minutes:int
    source_revision_id:str
    source_bar_hashes:tuple[str,...]
    reason_codes:tuple[str,...]
    semantic_hash:str
    def __post_init__(self):
        _req(self.aggregate_id,'aggregate_id');_req(self.descriptor_id,'descriptor_id');require_identifier(self.canonical_symbol,'canonical_symbol');_req(self.source_revision_id,'source_revision_id');require_sha256(self.semantic_hash,'semantic_hash')
        counts=(self.present_minutes,self.expected_elapsed_minutes,self.expected_total_minutes,self.missing_minutes,self.out_of_coverage_minutes,self.conflict_minutes)
        if any(x<0 for x in counts) or self.expected_elapsed_minutes>self.expected_total_minutes: raise FPI05Error('FP_RRC_WINDOW_COUNTS_INVALID','window counts invalid')
        if tuple(sorted(set(self.source_bar_hashes)))!=self.source_bar_hashes: raise FPI05Error('FP_RRC_BAR_HASHES_NONCANONICAL','bar hashes must be unique sorted')
        if self.present_minutes:
            for name,value in [('open',self.open),('high',self.high),('low',self.low),('close',self.close)]: _finite(value,name)
            if self.high < max(self.open,self.close) or self.low > min(self.open,self.close) or self.high < self.low: raise FPI05Error('FP_RRC_AGGREGATE_OHLC_INVALID','aggregate OHLC invalid')
            _minute(self.high_utc_ms,'high_utc_ms');_minute(self.low_utc_ms,'low_utc_ms')
        elif any(v is not None for v in (self.open,self.high,self.low,self.close,self.high_utc_ms,self.low_utc_ms)):
            raise FPI05Error('FP_RRC_EMPTY_AGGREGATE_HAS_PRICE','empty aggregate cannot carry prices')
    @property
    def coverage_ratio(self): return self.present_minutes/self.expected_elapsed_minutes if self.expected_elapsed_minutes else 0.0

@dataclass(frozen=True,slots=True)
class PairWindowAggregate:
    pair_window_id:str
    descriptor:WindowDescriptor
    left:SymbolWindowAggregate
    right:SymbolWindowAggregate
    health:PairWindowHealth
    source_revision_id:str
    reason_codes:tuple[str,...]
    semantic_hash:str
    def __post_init__(self):
        _req(self.pair_window_id,'pair_window_id');require_sha256(self.semantic_hash,'semantic_hash');_req(self.source_revision_id,'source_revision_id')
        if self.left.descriptor_id!=self.descriptor.descriptor_id or self.right.descriptor_id!=self.descriptor.descriptor_id: raise FPI05Error('FP_RRC_DESCRIPTOR_MISMATCH','aggregate descriptor mismatch')
        if self.left.canonical_symbol==self.right.canonical_symbol: raise FPI05Error('FP_RRC_PAIR_SYMBOLS_EQUAL','pair window symbols must differ')
    @property
    def completed(self): return self.left.state is WindowBuildState.COMPLETE and self.right.state is WindowBuildState.COMPLETE

@dataclass(frozen=True,slots=True)
class CalendarDaySelectionItem:
    offset:int
    target_date:str
    expected_window_kind:WindowKind
    disposition:SelectorDisposition
    pair_window_id:str
    descriptor_id:str
    reason_code:str
    evidence_hash:str
    def __post_init__(self):
        if self.offset<1: raise FPI05Error('FP_RRC_SELECTOR_OFFSET_INVALID','offset must be positive')
        _req(self.target_date,'target_date');_req(self.reason_code,'reason_code');require_sha256(self.evidence_hash,'evidence_hash')
        if self.disposition is SelectorDisposition.SELECTED and (not self.pair_window_id or not self.descriptor_id): raise FPI05Error('FP_RRC_SELECTED_WINDOW_REQUIRED','selected item requires window')

@dataclass(frozen=True,slots=True)
class CalendarDaySelection:
    selection_id:str
    anchor_trading_date:str
    depth:int
    items:tuple[CalendarDaySelectionItem,...]
    lookback_policy:LookbackPolicy
    store_snapshot_hash:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.selection_id,'selection_id');_req(self.anchor_trading_date,'anchor_trading_date');require_sha256(self.store_snapshot_hash,'store_snapshot_hash');require_sha256(self.evidence_hash,'evidence_hash')
        if self.depth!=len(self.items) or tuple(i.offset for i in self.items)!=tuple(range(1,self.depth+1)): raise FPI05Error('FP_RRC_SELECTOR_NONCONTIGUOUS','calendar offsets must be contiguous and uncompressed')

@dataclass(frozen=True,slots=True)
class ReferenceLevel:
    reference_id:str
    pair_id:str
    canonical_symbol:str
    side:PriceSide
    price:float
    extreme_utc_ms:int
    source_pair_window_id:str
    source_descriptor_id:str
    source_window_kind:WindowKind
    source_trading_date:str
    source_week_id:str
    source_revision_id:str
    state:ReferenceState
    state_sequence:int
    created_utc_ms:int
    last_transition_utc_ms:int
    reason_code:str
    semantic_hash:str
    def __post_init__(self):
        _req(self.reference_id,'reference_id');require_identifier(self.pair_id,'pair_id');require_identifier(self.canonical_symbol,'canonical_symbol');_finite(self.price,'price');_minute(self.extreme_utc_ms,'extreme_utc_ms')
        _req(self.source_pair_window_id,'source_pair_window_id');_req(self.source_descriptor_id,'source_descriptor_id');_req(self.source_trading_date,'source_trading_date');_req(self.source_revision_id,'source_revision_id');_req(self.reason_code,'reason_code');require_sha256(self.semantic_hash,'semantic_hash')
        if self.state_sequence<0 or self.created_utc_ms<0 or self.last_transition_utc_ms<self.created_utc_ms: raise FPI05Error('FP_RRC_REFERENCE_TIMELINE_INVALID','reference timeline invalid')
    @property
    def active_for_hunt(self): return self.state in (ReferenceState.FRESH,ReferenceState.HUNTER_SEEN)

@dataclass(frozen=True,slots=True)
class ReferenceTransitionRecord:
    event_id:str
    reference_id:str
    sequence:int
    transition:ReferenceTransition
    prior_state:ReferenceState
    next_state:ReferenceState
    actor:TouchActor|None
    event_utc_ms:int
    evidence_id:str
    reason_code:str
    event_hash:str
    def __post_init__(self):
        _req(self.event_id,'event_id');_req(self.reference_id,'reference_id');_req(self.evidence_id,'evidence_id');_req(self.reason_code,'reason_code');require_sha256(self.event_hash,'event_hash')
        if self.sequence<1 or self.event_utc_ms<0 or self.event_utc_ms%M1_MS: raise FPI05Error('FP_RRC_REFERENCE_EVENT_INVALID','reference event must be positive sequence on UTC M1')

@dataclass(frozen=True,slots=True)
class ReferenceSet:
    reference_set_id:str
    pair_window_id:str
    references:tuple[ReferenceLevel,...]
    source_revision_id:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.reference_set_id,'reference_set_id');_req(self.pair_window_id,'pair_window_id');_req(self.source_revision_id,'source_revision_id');require_sha256(self.evidence_hash,'evidence_hash')
        keys=[(r.canonical_symbol,r.side) for r in self.references]
        if len(keys)!=len(set(keys)): raise FPI05Error('FP_RRC_REFERENCE_DUPLICATE','duplicate symbol-side reference')

@dataclass(frozen=True,slots=True)
class WindowStoreSnapshot:
    snapshot_id:str
    pair_id:str
    config_hash:str
    source_dataset_snapshot_id:str
    source_revision_id:str
    pair_windows:tuple[PairWindowAggregate,...]
    references:tuple[ReferenceLevel,...]
    health:StoreHealth
    reason_codes:tuple[str,...]
    created_utc_ms:int
    index_hash:str
    semantic_hash:str
    def __post_init__(self):
        _req(self.snapshot_id,'snapshot_id');require_identifier(self.pair_id,'pair_id');require_sha256(self.config_hash,'config_hash');_req(self.source_dataset_snapshot_id,'source_dataset_snapshot_id');_req(self.source_revision_id,'source_revision_id');require_sha256(self.index_hash,'index_hash');require_sha256(self.semantic_hash,'semantic_hash')
        if self.created_utc_ms<0: raise FPI05Error('FP_RRC_SNAPSHOT_TIME_INVALID','snapshot time invalid')
        if len({w.pair_window_id for w in self.pair_windows})!=len(self.pair_windows): raise FPI05Error('FP_RRC_WINDOW_DUPLICATE','duplicate pair window')
        keys=[(w.descriptor.trading_date,w.descriptor.kind) for w in self.pair_windows]
        if len(keys)!=len(set(keys)): raise FPI05Error('FP_RRC_WINDOW_INDEX_COLLISION','duplicate trading-date/kind window key')
        if len({r.reference_id for r in self.references})!=len(self.references): raise FPI05Error('FP_RRC_REFERENCE_DUPLICATE','duplicate reference id')

@dataclass(frozen=True,slots=True)
class RevisionInvalidation:
    invalidation_id:str
    revision_id:str
    affected_pair_window_ids:tuple[str,...]
    affected_reference_ids:tuple[str,...]
    unchanged_prefix_hash:str
    reason_code:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.invalidation_id,'invalidation_id');_req(self.revision_id,'revision_id');require_sha256(self.unchanged_prefix_hash,'unchanged_prefix_hash');_req(self.reason_code,'reason_code');require_sha256(self.evidence_hash,'evidence_hash')

@dataclass(frozen=True,slots=True)
class WindowStoreCheckpoint:
    checkpoint_id:str
    checkpoint_version:str
    config_hash:str
    source_revision_id:str
    snapshot_semantic_hash:str
    payload_hash:str
    created_utc_ms:int
    def __post_init__(self):
        _req(self.checkpoint_id,'checkpoint_id');require_semver(self.checkpoint_version,'checkpoint_version');require_sha256(self.config_hash,'config_hash');_req(self.source_revision_id,'source_revision_id');require_sha256(self.snapshot_semantic_hash,'snapshot_semantic_hash');require_sha256(self.payload_hash,'payload_hash')
