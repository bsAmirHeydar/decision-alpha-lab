from __future__ import annotations
from dataclasses import dataclass, field
import math
from typing import Mapping
from .canonical import canonical_sha256, stable_id, require_identifier, require_semver, require_sha256
from .constants import *
from .enums import *
from .errors import FPI04Error

def _req(v,n):
    if not isinstance(v,str) or not v.strip(): raise FPI04Error('FP_DRC_REQUIRED_FIELD',f'{n} is required',{'field':n})
    return v

def _minute(v,n='open_utc_ms'):
    if not isinstance(v,int) or v<0 or v%M1_MS: raise FPI04Error('FP_DRC_M1_ALIGNMENT_INVALID',f'{n} must be non-negative UTC minute open')
    return v

def _finite(v,n):
    if not isinstance(v,(int,float)) or not math.isfinite(float(v)): raise FPI04Error('FP_DRC_NONFINITE_PRICE',f'{n} must be finite')
    return float(v)

@dataclass(frozen=True,slots=True)
class SymbolSpec:
    canonical_symbol:str
    aliases:tuple[str,...]
    tick_size:float
    digits:int
    contract_version:str=SYMBOL_RESOLVER_VERSION
    def __post_init__(self):
        require_identifier(self.canonical_symbol,'canonical_symbol'); require_semver(self.contract_version,'contract_version')
        aliases=tuple(a.strip() for a in self.aliases)
        if not aliases or any(not a or len(a)>MAX_SYMBOL_LENGTH for a in aliases): raise FPI04Error('FP_DRC_ALIAS_INVALID','aliases invalid')
        if len(set(a.upper() for a in aliases))!=len(aliases): raise FPI04Error('FP_DRC_ALIAS_DUPLICATE','aliases must be unique case-insensitively')
        if _finite(self.tick_size,'tick_size')<=0: raise FPI04Error('FP_DRC_TICK_SIZE_INVALID','tick size must be positive')
        if self.digits<0 or self.digits>12: raise FPI04Error('FP_DRC_DIGITS_INVALID','digits outside [0,12]')
    @property
    def spec_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class SymbolPairSpec:
    context_id:str
    pair_id:str
    left:SymbolSpec
    right:SymbolSpec
    resolver_version:str=SYMBOL_RESOLVER_VERSION
    def __post_init__(self):
        require_identifier(self.context_id,'context_id'); require_identifier(self.pair_id,'pair_id'); require_semver(self.resolver_version,'resolver_version')
        if self.left.canonical_symbol==self.right.canonical_symbol: raise FPI04Error('FP_DRC_PAIR_SYMBOLS_EQUAL','pair symbols must differ')
    @property
    def pair_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class M1Bar:
    canonical_symbol:str
    open_utc_ms:int
    open:float
    high:float
    low:float
    close:float
    tick_volume:int
    real_volume:int
    spread_points:int
    finality:BarFinality
    source_id:str
    source_sequence:int
    source_revision:str
    received_utc_ms:int
    contract_version:str=BAR_CONTRACT_VERSION
    def __post_init__(self):
        require_identifier(self.canonical_symbol,'canonical_symbol'); _minute(self.open_utc_ms)
        o,h,l,c=(_finite(self.open,'open'),_finite(self.high,'high'),_finite(self.low,'low'),_finite(self.close,'close'))
        if h<l or h<max(o,c) or l>min(o,c): raise FPI04Error('FP_DRC_OHLC_INVALID','OHLC envelope invalid')
        if self.tick_volume<0 or self.real_volume<0 or self.spread_points<0: raise FPI04Error('FP_DRC_VOLUME_SPREAD_INVALID','volume/spread cannot be negative')
        _req(self.source_id,'source_id'); _req(self.source_revision,'source_revision'); require_semver(self.contract_version,'contract_version')
        if self.source_sequence<0 or self.received_utc_ms<self.open_utc_ms: raise FPI04Error('FP_DRC_SOURCE_ORDER_INVALID','source sequence or received time invalid')
    @property
    def semantic_payload(self):
        return {'canonical_symbol':self.canonical_symbol,'open_utc_ms':self.open_utc_ms,'open':self.open,'high':self.high,'low':self.low,'close':self.close,'tick_volume':self.tick_volume,'real_volume':self.real_volume,'spread_points':self.spread_points,'finality':self.finality,'source_revision':self.source_revision,'contract_version':self.contract_version}
    @property
    def bar_hash(self): return canonical_sha256(self.semantic_payload)
    @property
    def bar_id(self): return stable_id('FPM1',self.semantic_payload,32)

@dataclass(frozen=True,slots=True)
class DuplicateResolution:
    canonical_symbol:str
    open_utc_ms:int
    disposition:DuplicateDisposition
    selected_bar:M1Bar|None
    input_hashes:tuple[str,...]
    reason_code:str
    evidence_hash:str
    def __post_init__(self):
        require_identifier(self.canonical_symbol,'canonical_symbol'); _minute(self.open_utc_ms); _req(self.reason_code,'reason_code'); require_sha256(self.evidence_hash,'evidence_hash')
        if tuple(sorted(set(self.input_hashes)))!=self.input_hashes: raise FPI04Error('FP_DRC_HASH_LIST_NONCANONICAL','input hashes must be unique ascending')
        if self.disposition is DuplicateDisposition.CONFLICT and self.selected_bar is not None: raise FPI04Error('FP_DRC_CONFLICT_SELECTED_BAR','conflict cannot select bar')
        if self.disposition is not DuplicateDisposition.CONFLICT and self.selected_bar is None: raise FPI04Error('FP_DRC_SELECTED_BAR_REQUIRED','non-conflict requires selected bar')

@dataclass(frozen=True,slots=True)
class CoverageInterval:
    canonical_symbol:str
    start_utc_ms:int
    end_utc_ms:int
    present_minutes:int
    expected_minutes:int
    calendar_excluded_minutes:int
    state:CoverageState
    source_revision_hash:str
    reason_code:str
    def __post_init__(self):
        require_identifier(self.canonical_symbol,'canonical_symbol'); _minute(self.start_utc_ms,'start_utc_ms'); _minute(self.end_utc_ms,'end_utc_ms')
        total=(self.end_utc_ms-self.start_utc_ms)//M1_MS
        if self.end_utc_ms<=self.start_utc_ms or self.expected_minutes<0 or self.calendar_excluded_minutes<0 or self.expected_minutes+self.calendar_excluded_minutes!=total: raise FPI04Error('FP_DRC_COVERAGE_INTERVAL_INVALID','coverage interval invalid')
        if self.present_minutes<0 or self.present_minutes>self.expected_minutes: raise FPI04Error('FP_DRC_COVERAGE_COUNT_INVALID','coverage count invalid')
        require_sha256(self.source_revision_hash,'source_revision_hash'); _req(self.reason_code,'reason_code')
    @property
    def coverage_ratio(self): return self.present_minutes/self.expected_minutes if self.expected_minutes else 0.0
    @property
    def interval_id(self): return stable_id('FPCOV',self,32)

@dataclass(frozen=True,slots=True)
class GapInterval:
    canonical_symbol:str
    start_utc_ms:int
    end_utc_ms:int
    missing_minutes:int
    reason:GapReason
    first_detected_revision:str
    evidence_hash:str
    def __post_init__(self):
        require_identifier(self.canonical_symbol,'canonical_symbol'); _minute(self.start_utc_ms,'start_utc_ms'); _minute(self.end_utc_ms,'end_utc_ms')
        if self.end_utc_ms<=self.start_utc_ms or self.missing_minutes!=(self.end_utc_ms-self.start_utc_ms)//M1_MS: raise FPI04Error('FP_DRC_GAP_INTERVAL_INVALID','gap interval invalid')
        _req(self.first_detected_revision,'first_detected_revision'); require_sha256(self.evidence_hash,'evidence_hash')
    @property
    def gap_id(self): return stable_id('FPGAP',self,32)

@dataclass(frozen=True,slots=True)
class MinuteCell:
    canonical_symbol:str
    open_utc_ms:int
    state:MinuteCellState
    bar:M1Bar|None
    reason_code:str
    source_revision_hash:str
    def __post_init__(self):
        require_identifier(self.canonical_symbol,'canonical_symbol'); _minute(self.open_utc_ms); _req(self.reason_code,'reason_code'); require_sha256(self.source_revision_hash,'source_revision_hash')
        if self.state in (MinuteCellState.PRESENT,MinuteCellState.REVISED) and self.bar is None: raise FPI04Error('FP_DRC_CELL_BAR_REQUIRED','present/revised cell needs bar')
        if self.state not in (MinuteCellState.PRESENT,MinuteCellState.REVISED) and self.bar is not None: raise FPI04Error('FP_DRC_CELL_BAR_FORBIDDEN','non-present cell cannot carry bar')
    @property
    def cell_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class AlignedMinute:
    pair_id:str
    open_utc_ms:int
    left:MinuteCell
    right:MinuteCell
    calendar_segment:str
    calendar_snapshot_hash:str
    synchronization_version:str=SYNCHRONIZER_VERSION
    def __post_init__(self):
        require_identifier(self.pair_id,'pair_id'); _minute(self.open_utc_ms)
        if self.left.open_utc_ms!=self.open_utc_ms or self.right.open_utc_ms!=self.open_utc_ms: raise FPI04Error('FP_DRC_ALIGNMENT_TIME_MISMATCH','cell minute mismatch')
        require_sha256(self.calendar_snapshot_hash,'calendar_snapshot_hash'); require_semver(self.synchronization_version,'synchronization_version')
    @property
    def both_present(self): return self.left.state in (MinuteCellState.PRESENT,MinuteCellState.REVISED) and self.right.state in (MinuteCellState.PRESENT,MinuteCellState.REVISED)
    @property
    def row_id(self): return stable_id('FPALIGN',self,32)

@dataclass(frozen=True,slots=True)
class DataRevision:
    revision_id:str
    pair_id:str
    parent_revision_id:str
    kind:RevisionKind
    changed_symbols:tuple[str,...]
    affected_start_utc_ms:int
    affected_end_utc_ms:int
    previous_payload_hash:str
    current_payload_hash:str
    created_utc_ms:int
    reason_code:str
    revision_version:str=REVISION_VERSION
    def __post_init__(self):
        _req(self.revision_id,'revision_id'); require_identifier(self.pair_id,'pair_id'); _req(self.parent_revision_id,'parent_revision_id')
        if tuple(sorted(set(self.changed_symbols)))!=self.changed_symbols: raise FPI04Error('FP_DRC_CHANGED_SYMBOLS_NONCANONICAL','changed symbols must be unique sorted')
        _minute(self.affected_start_utc_ms,'affected_start_utc_ms'); _minute(self.affected_end_utc_ms,'affected_end_utc_ms')
        if self.affected_end_utc_ms<self.affected_start_utc_ms: raise FPI04Error('FP_DRC_REVISION_RANGE_INVALID','revision range invalid')
        require_sha256(self.previous_payload_hash,'previous_payload_hash'); require_sha256(self.current_payload_hash,'current_payload_hash'); require_semver(self.revision_version,'revision_version'); _req(self.reason_code,'reason_code')
    @property
    def revision_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class IncrementalCursor:
    pair_id:str
    last_emitted_open_utc_ms:int|None
    left_last_source_sequence:int
    right_last_source_sequence:int
    data_revision_id:str
    state:CursorState
    cursor_version:str=CURSOR_VERSION
    def __post_init__(self):
        require_identifier(self.pair_id,'pair_id'); _req(self.data_revision_id,'data_revision_id'); require_semver(self.cursor_version,'cursor_version')
        if self.last_emitted_open_utc_ms is not None: _minute(self.last_emitted_open_utc_ms,'last_emitted_open_utc_ms')
        if self.left_last_source_sequence< -1 or self.right_last_source_sequence< -1: raise FPI04Error('FP_DRC_CURSOR_SEQUENCE_INVALID','cursor source sequence invalid')
    @property
    def cursor_id(self): return stable_id('FPCURSOR',self,32)

@dataclass(frozen=True,slots=True)
class BackfillRequest:
    request_id:str
    canonical_symbol:str
    start_utc_ms:int
    end_utc_ms:int
    requested_minutes:int
    action:BackfillAction
    reason_code:str
    priority:int
    policy_version:str=BACKFILL_VERSION
    def __post_init__(self):
        _req(self.request_id,'request_id'); require_identifier(self.canonical_symbol,'canonical_symbol'); _minute(self.start_utc_ms,'start_utc_ms'); _minute(self.end_utc_ms,'end_utc_ms')
        if self.end_utc_ms<=self.start_utc_ms or self.requested_minutes!=(self.end_utc_ms-self.start_utc_ms)//M1_MS: raise FPI04Error('FP_DRC_BACKFILL_RANGE_INVALID','backfill range invalid')
        if self.priority<0: raise FPI04Error('FP_DRC_BACKFILL_PRIORITY_INVALID','priority invalid')
        _req(self.reason_code,'reason_code'); require_semver(self.policy_version,'policy_version')

@dataclass(frozen=True,slots=True)
class SynchronizationResult:
    result_id:str
    pair_id:str
    start_utc_ms:int
    end_utc_ms:int
    rows:tuple[AlignedMinute,...]
    left_coverage:CoverageInterval
    right_coverage:CoverageInterval
    gaps:tuple[GapInterval,...]
    conflicts:tuple[DuplicateResolution,...]
    revision:DataRevision
    health:SynchronizationHealth
    reason_codes:tuple[str,...]
    semantic_hash:str
    def __post_init__(self):
        _req(self.result_id,'result_id'); require_identifier(self.pair_id,'pair_id'); _minute(self.start_utc_ms,'start_utc_ms'); _minute(self.end_utc_ms,'end_utc_ms')
        if self.end_utc_ms<=self.start_utc_ms: raise FPI04Error('FP_DRC_SYNC_RANGE_INVALID','sync range invalid')
        if tuple(sorted(self.rows,key=lambda r:r.open_utc_ms))!=self.rows or len({r.open_utc_ms for r in self.rows})!=len(self.rows): raise FPI04Error('FP_DRC_ROWS_NONCANONICAL','rows must be unique ascending')
        if tuple(sorted(set(self.reason_codes)))!=self.reason_codes: raise FPI04Error('FP_DRC_REASON_LIST_NONCANONICAL','reason codes must be unique ascending')
        require_sha256(self.semantic_hash,'semantic_hash')
    @property
    def emitted_minutes(self): return len(self.rows)
    @property
    def both_present_minutes(self): return sum(1 for r in self.rows if r.both_present)

@dataclass(frozen=True,slots=True)
class RevisionImpact:
    revision_id:str
    affected_minute_ids:tuple[int,...]
    affected_window_ids:tuple[str,...]
    unaffected_prefix_hash:str
    changed_suffix_hash:str
    reason_code:str
    def __post_init__(self):
        _req(self.revision_id,'revision_id');
        if tuple(sorted(set(self.affected_minute_ids)))!=self.affected_minute_ids: raise FPI04Error('FP_DRC_AFFECTED_MINUTES_NONCANONICAL','affected minutes must be unique sorted')
        if tuple(sorted(set(self.affected_window_ids)))!=self.affected_window_ids: raise FPI04Error('FP_DRC_AFFECTED_WINDOWS_NONCANONICAL','affected windows must be unique sorted')
        require_sha256(self.unaffected_prefix_hash,'unaffected_prefix_hash'); require_sha256(self.changed_suffix_hash,'changed_suffix_hash'); _req(self.reason_code,'reason_code')

@dataclass(frozen=True,slots=True)
class SynchronizerConfig:
    context_id:str='FP-CONTEXT-001'
    pair_id:str='FP-PAIR-PRIMARY'
    expected_minute_policy:ExpectedMinutePolicy=ExpectedMinutePolicy.NY_TRADING_SESSIONS_ONLY
    closed_bars_only:bool=True
    maximum_backfill_minutes:int=DEFAULT_MAX_BACKFILL_MINUTES
    maximum_gap_run_minutes:int=DEFAULT_MAX_GAP_RUN_MINUTES
    kernel_version:str=KERNEL_VERSION
    calendar_config_hash:str='0'*64
    def __post_init__(self):
        require_identifier(self.context_id,'context_id'); require_identifier(self.pair_id,'pair_id'); require_semver(self.kernel_version,'kernel_version'); require_sha256(self.calendar_config_hash,'calendar_config_hash')
        if self.maximum_backfill_minutes<1 or self.maximum_gap_run_minutes<1: raise FPI04Error('FP_DRC_CONFIG_LIMIT_INVALID','config limits must be positive')
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class PairDatasetSnapshot:
    snapshot_id:str
    pair_id:str
    start_utc_ms:int
    end_utc_ms:int
    row_ids:tuple[str,...]
    semantic_hash:str
    data_revision_id:str
    created_utc_ms:int
    health:SynchronizationHealth
    reason_codes:tuple[str,...]
    def __post_init__(self):
        _req(self.snapshot_id,'snapshot_id'); require_identifier(self.pair_id,'pair_id'); _minute(self.start_utc_ms,'start_utc_ms'); _minute(self.end_utc_ms,'end_utc_ms')
        if self.end_utc_ms<=self.start_utc_ms: raise FPI04Error('FP_DRC_SNAPSHOT_RANGE_INVALID','snapshot range invalid')
        if len(set(self.row_ids))!=len(self.row_ids): raise FPI04Error('FP_DRC_SNAPSHOT_ROW_DUPLICATE','row IDs duplicate')
        require_sha256(self.semantic_hash,'semantic_hash'); _req(self.data_revision_id,'data_revision_id')
        if tuple(sorted(set(self.reason_codes)))!=self.reason_codes: raise FPI04Error('FP_DRC_REASON_LIST_NONCANONICAL','reasons noncanonical')
