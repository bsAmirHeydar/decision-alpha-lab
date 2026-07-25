from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Mapping
from fp_i02_kernel.enums import RelationCode, WindowKind, PriceSide, Direction, SymbolRole, ReferenceState
from fp_i05_reference.contracts import ReferenceLevel
from .canonical import canonical_sha256, stable_id, require_identifier, require_semver, require_sha256
from .constants import *
from .enums import *
from .errors import FPI06Error

def _req(value,name):
    if not isinstance(value,str) or not value.strip(): raise FPI06Error("FP_HRC_REQUIRED_FIELD",f"{name} is required",{"field":name})
    return value

def _minute(value,name):
    if not isinstance(value,int) or value<0 or value%M1_MS: raise FPI06Error("FP_HRC_MINUTE_INVALID",f"{name} must be UTC M1 aligned")
    return value

def _finite(value,name):
    if not isinstance(value,(int,float)) or not math.isfinite(float(value)): raise FPI06Error("FP_HRC_NONFINITE_VALUE",f"{name} must be finite")
    return float(value)

@dataclass(frozen=True,slots=True)
class RelationDescriptor:
    relation:RelationCode
    family:RelationFamily
    reference_kind:WindowKind
    check_kind:WindowKind
    historical_selector_required:bool
    calendar_offset_required:bool
    directly_tradeable:bool
    supported_in_phase:bool
    version:str=RELATION_REGISTRY_VERSION
    def __post_init__(self):
        require_semver(self.version,"version")
        if self.relation is RelationCode.WW and self.supported_in_phase: raise FPI06Error("FP_HRC_WW_DEFERRED","WW is deferred to FP-I08")
        if self.calendar_offset_required and not self.historical_selector_required: raise FPI06Error("FP_HRC_DESCRIPTOR_INVALID","calendar offset requires selector")
    @property
    def descriptor_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class RelationCompilerConfig:
    context_id:str
    pair_id:str
    relation_registry_hash:str
    reference_store_hash:str
    hunt_engine_version:str=HUNT_ENGINE_VERSION
    candidate_engine_version:str=CANDIDATE_ENGINE_VERSION
    enabled_relations:tuple[RelationCode,...]=(RelationCode.AL,RelationCode.AN,RelationCode.LN,RelationCode.NA,RelationCode.NL,RelationCode.NN)
    def __post_init__(self):
        require_identifier(self.context_id,"context_id");require_identifier(self.pair_id,"pair_id")
        require_sha256(self.relation_registry_hash,"relation_registry_hash");require_sha256(self.reference_store_hash,"reference_store_hash")
        require_semver(self.hunt_engine_version,"hunt_engine_version");require_semver(self.candidate_engine_version,"candidate_engine_version")
        if tuple(sorted(set(self.enabled_relations),key=lambda x:x.value))!=tuple(sorted(self.enabled_relations,key=lambda x:x.value)): raise FPI06Error("FP_HRC_RELATION_SET_NONCANONICAL","enabled relations must be unique canonical order")
        if RelationCode.WW in self.enabled_relations: raise FPI06Error("FP_HRC_WW_DEFERRED","WW cannot be enabled in FP-I06")
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class RelationInstance:
    relation_instance_id:str
    relation:RelationCode
    pair_id:str
    anchor_trading_date:str
    calendar_offset:int
    reference_pair_window_id:str
    reference_descriptor_id:str
    reference_window_kind:WindowKind
    reference_trading_date:str
    check_pair_window_id:str
    check_descriptor_id:str
    check_window_kind:WindowKind
    check_start_utc_ms:int
    check_end_utc_ms:int
    source_store_snapshot_hash:str
    source_revision_id:str
    state:RelationInstanceState
    reason_codes:tuple[str,...]
    semantic_hash:str
    def __post_init__(self):
        _req(self.relation_instance_id,"relation_instance_id");require_identifier(self.pair_id,"pair_id");_req(self.anchor_trading_date,"anchor_trading_date")
        _req(self.reference_pair_window_id,"reference_pair_window_id");_req(self.reference_descriptor_id,"reference_descriptor_id");_req(self.reference_trading_date,"reference_trading_date")
        _req(self.check_pair_window_id,"check_pair_window_id");_req(self.check_descriptor_id,"check_descriptor_id");_minute(self.check_start_utc_ms,"check_start_utc_ms");_minute(self.check_end_utc_ms,"check_end_utc_ms")
        if self.check_end_utc_ms<=self.check_start_utc_ms: raise FPI06Error("FP_HRC_CHECK_WINDOW_INVALID","check window interval invalid")
        require_sha256(self.source_store_snapshot_hash,"source_store_snapshot_hash");_req(self.source_revision_id,"source_revision_id");require_sha256(self.semantic_hash,"semantic_hash")
        if self.relation in (RelationCode.NA,RelationCode.NL,RelationCode.NN) and self.calendar_offset<1: raise FPI06Error("FP_HRC_CALENDAR_OFFSET_REQUIRED","historical N relation requires positive offset")
        if self.relation in (RelationCode.AL,RelationCode.AN,RelationCode.LN) and self.calendar_offset!=0: raise FPI06Error("FP_HRC_CALENDAR_OFFSET_FORBIDDEN","same-day relation offset must be zero")

@dataclass(frozen=True,slots=True)
class RelationSidePlan:
    side_plan_id:str
    relation_instance_id:str
    relation:RelationCode
    side:PriceSide
    left_reference_id:str
    left_symbol:str
    left_reference_price:float
    right_reference_id:str
    right_symbol:str
    right_reference_price:float
    check_start_utc_ms:int
    check_end_utc_ms:int
    state:SidePlanState
    reason_codes:tuple[str,...]
    source_reference_hashes:tuple[str,...]
    semantic_hash:str
    def __post_init__(self):
        _req(self.side_plan_id,"side_plan_id");_req(self.relation_instance_id,"relation_instance_id");_req(self.left_reference_id,"left_reference_id");require_identifier(self.left_symbol,"left_symbol")
        _req(self.right_reference_id,"right_reference_id");require_identifier(self.right_symbol,"right_symbol")
        if self.left_symbol==self.right_symbol: raise FPI06Error("FP_HRC_PAIR_SYMBOLS_EQUAL","side plan symbols must differ")
        _finite(self.left_reference_price,"left_reference_price");_finite(self.right_reference_price,"right_reference_price")
        _minute(self.check_start_utc_ms,"check_start_utc_ms");_minute(self.check_end_utc_ms,"check_end_utc_ms")
        if tuple(sorted(set(self.source_reference_hashes)))!=self.source_reference_hashes or len(self.source_reference_hashes)!=2: raise FPI06Error("FP_HRC_REFERENCE_HASHES_NONCANONICAL","exactly two unique sorted reference hashes required")
        require_sha256(self.semantic_hash,"semantic_hash")

@dataclass(frozen=True,slots=True)
class HuntFact:
    hunt_fact_id:str
    side_plan_id:str
    relation_instance_id:str
    canonical_symbol:str
    side:PriceSide
    reference_id:str
    reference_price:float
    hunt_minute_utc_ms:int
    bar_hash:str
    observed_extreme:float
    source_revision_id:str
    reason_code:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.hunt_fact_id,"hunt_fact_id");_req(self.side_plan_id,"side_plan_id");_req(self.relation_instance_id,"relation_instance_id");require_identifier(self.canonical_symbol,"canonical_symbol")
        _req(self.reference_id,"reference_id");_finite(self.reference_price,"reference_price");_minute(self.hunt_minute_utc_ms,"hunt_minute_utc_ms");require_sha256(self.bar_hash,"bar_hash");_finite(self.observed_extreme,"observed_extreme");_req(self.source_revision_id,"source_revision_id");_req(self.reason_code,"reason_code");require_sha256(self.evidence_hash,"evidence_hash")
        if self.side is PriceSide.HIGH and self.observed_extreme < self.reference_price: raise FPI06Error("FP_HRC_FALSE_HIGH_CONTACT","high hunt fact did not reach reference")
        if self.side is PriceSide.LOW and self.observed_extreme > self.reference_price: raise FPI06Error("FP_HRC_FALSE_LOW_CONTACT","low hunt fact did not reach reference")

@dataclass(frozen=True,slots=True)
class MinuteContactObservation:
    observation_id:str
    side_plan_id:str
    minute_utc_ms:int
    contact_state:ContactState
    left_hunt_fact_id:str
    right_hunt_fact_id:str
    source_row_id:str
    source_revision_hash:str
    reason_code:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.observation_id,"observation_id");_req(self.side_plan_id,"side_plan_id");_minute(self.minute_utc_ms,"minute_utc_ms");_req(self.source_row_id,"source_row_id");require_sha256(self.source_revision_hash,"source_revision_hash");_req(self.reason_code,"reason_code");require_sha256(self.evidence_hash,"evidence_hash")
        if self.contact_state is ContactState.LEFT_ONLY and (not self.left_hunt_fact_id or self.right_hunt_fact_id): raise FPI06Error("FP_HRC_CONTACT_FACT_MISMATCH","LEFT_ONLY fact mismatch")
        if self.contact_state is ContactState.RIGHT_ONLY and (not self.right_hunt_fact_id or self.left_hunt_fact_id): raise FPI06Error("FP_HRC_CONTACT_FACT_MISMATCH","RIGHT_ONLY fact mismatch")
        if self.contact_state is ContactState.BOTH_SAME_M1 and (not self.left_hunt_fact_id or not self.right_hunt_fact_id): raise FPI06Error("FP_HRC_CONTACT_FACT_MISMATCH","BOTH requires two facts")

@dataclass(frozen=True,slots=True)
class FirstSweepClassification:
    classification_id:str
    side_plan_id:str
    relation_instance_id:str
    outcome:SweepOutcome
    first_hunt_minute_utc_ms:int|None
    hunter_symbol:str
    protected_symbol:str
    hunter_hunt_fact_id:str
    symmetric_fact_ids:tuple[str,...]
    data_block_minute_utc_ms:int|None
    reason_code:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.classification_id,"classification_id");_req(self.side_plan_id,"side_plan_id");_req(self.relation_instance_id,"relation_instance_id");_req(self.reason_code,"reason_code");require_sha256(self.evidence_hash,"evidence_hash")
        if self.first_hunt_minute_utc_ms is not None:_minute(self.first_hunt_minute_utc_ms,"first_hunt_minute_utc_ms")
        if self.data_block_minute_utc_ms is not None:_minute(self.data_block_minute_utc_ms,"data_block_minute_utc_ms")
        if self.outcome in (SweepOutcome.LEFT_FIRST,SweepOutcome.RIGHT_FIRST):
            require_identifier(self.hunter_symbol,"hunter_symbol");require_identifier(self.protected_symbol,"protected_symbol");_req(self.hunter_hunt_fact_id,"hunter_hunt_fact_id")
            if self.hunter_symbol==self.protected_symbol: raise FPI06Error("FP_HRC_ROLE_COLLISION","hunter and protected symbols must differ")
        if self.outcome is SweepOutcome.SYMMETRIC_SAME_M1 and len(self.symmetric_fact_ids)!=2: raise FPI06Error("FP_HRC_SYMMETRIC_FACT_COUNT","same-M1 symmetric classification requires two facts")

@dataclass(frozen=True,slots=True)
class RawDivergenceCandidate:
    candidate_id:str
    side_plan_id:str
    relation_instance_id:str
    relation:RelationCode
    direction:Direction
    side:PriceSide
    hunter_symbol:str
    protected_symbol:str
    first_hunt_minute_utc_ms:int
    hunter_hunt_fact_id:str
    state:CandidateState
    state_sequence:int
    second_touch_minute_utc_ms:int|None
    second_touch_fact_id:str
    check_end_utc_ms:int
    source_revision_id:str
    reason_code:str
    semantic_hash:str
    def __post_init__(self):
        _req(self.candidate_id,"candidate_id");_req(self.side_plan_id,"side_plan_id");_req(self.relation_instance_id,"relation_instance_id");require_identifier(self.hunter_symbol,"hunter_symbol");require_identifier(self.protected_symbol,"protected_symbol")
        if self.hunter_symbol==self.protected_symbol: raise FPI06Error("FP_HRC_ROLE_COLLISION","candidate roles collide")
        _minute(self.first_hunt_minute_utc_ms,"first_hunt_minute_utc_ms");_req(self.hunter_hunt_fact_id,"hunter_hunt_fact_id");_minute(self.check_end_utc_ms,"check_end_utc_ms");_req(self.source_revision_id,"source_revision_id");_req(self.reason_code,"reason_code");require_sha256(self.semantic_hash,"semantic_hash")
        expected=Direction.BULLISH if self.side is PriceSide.LOW else Direction.BEARISH
        if self.direction is not expected: raise FPI06Error("FP_HRC_DIRECTION_SIDE_MISMATCH","LOW must be bullish and HIGH bearish")
        if self.state_sequence<0: raise FPI06Error("FP_HRC_STATE_SEQUENCE_INVALID","state sequence cannot be negative")
        if self.second_touch_minute_utc_ms is not None:
            _minute(self.second_touch_minute_utc_ms,"second_touch_minute_utc_ms")
            if self.second_touch_minute_utc_ms<=self.first_hunt_minute_utc_ms: raise FPI06Error("FP_HRC_SECOND_TOUCH_ORDER_INVALID","second touch must be later M1")

@dataclass(frozen=True,slots=True)
class CandidateTransitionRecord:
    event_id:str
    candidate_id:str
    sequence:int
    transition:CandidateTransition
    prior_state:CandidateState|None
    next_state:CandidateState
    event_utc_ms:int
    evidence_id:str
    reason_code:str
    event_hash:str
    def __post_init__(self):
        _req(self.event_id,"event_id");_req(self.candidate_id,"candidate_id");_req(self.evidence_id,"evidence_id");_req(self.reason_code,"reason_code");require_sha256(self.event_hash,"event_hash");_minute(self.event_utc_ms,"event_utc_ms")
        if self.sequence<0: raise FPI06Error("FP_HRC_EVENT_SEQUENCE_INVALID","event sequence invalid")

@dataclass(frozen=True,slots=True)
class RelationScanResult:
    scan_id:str
    side_plan_id:str
    scan_mode:ScanMode
    scanned_start_utc_ms:int
    scanned_end_utc_ms:int
    observations:tuple[MinuteContactObservation,...]
    hunt_facts:tuple[HuntFact,...]
    classification:FirstSweepClassification
    candidate:RawDivergenceCandidate|None
    candidate_events:tuple[CandidateTransitionRecord,...]
    processed_row_count:int
    source_revision_id:str
    source_rows_hash:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.scan_id,"scan_id");_req(self.side_plan_id,"side_plan_id");_minute(self.scanned_start_utc_ms,"scanned_start_utc_ms");_minute(self.scanned_end_utc_ms,"scanned_end_utc_ms")
        if self.scanned_end_utc_ms<self.scanned_start_utc_ms or self.processed_row_count<0: raise FPI06Error("FP_HRC_SCAN_RANGE_INVALID","scan range/count invalid")
        _req(self.source_revision_id,"source_revision_id");require_sha256(self.source_rows_hash,"source_rows_hash");require_sha256(self.evidence_hash,"evidence_hash")
        if len({f.hunt_fact_id for f in self.hunt_facts})!=len(self.hunt_facts): raise FPI06Error("FP_HRC_DUPLICATE_HUNT_FACT","duplicate hunt fact")

@dataclass(frozen=True,slots=True)
class RelationCompilationReport:
    report_id:str
    anchor_trading_date:str
    compiled_instances:tuple[RelationInstance,...]
    side_plans:tuple[RelationSidePlan,...]
    skipped_relations:tuple[str,...]
    blocked_items:tuple[str,...]
    source_store_snapshot_hash:str
    relation_registry_hash:str
    evidence_hash:str
    def __post_init__(self):
        _req(self.report_id,"report_id");_req(self.anchor_trading_date,"anchor_trading_date");require_sha256(self.source_store_snapshot_hash,"source_store_snapshot_hash");require_sha256(self.relation_registry_hash,"relation_registry_hash");require_sha256(self.evidence_hash,"evidence_hash")
        if len({i.relation_instance_id for i in self.compiled_instances})!=len(self.compiled_instances): raise FPI06Error("FP_HRC_DUPLICATE_RELATION_INSTANCE","duplicate relation instance")
        if len({p.side_plan_id for p in self.side_plans})!=len(self.side_plans): raise FPI06Error("FP_HRC_DUPLICATE_SIDE_PLAN","duplicate side plan")

@dataclass(frozen=True,slots=True)
class ScanCursor:
    side_plan_id:str
    next_open_utc_ms:int
    source_revision_id:str
    source_rows_hash:str
    candidate_id:str
    candidate_state:CandidateState|None
    cursor_hash:str
    def __post_init__(self):
        _req(self.side_plan_id,"side_plan_id");_minute(self.next_open_utc_ms,"next_open_utc_ms");_req(self.source_revision_id,"source_revision_id");require_sha256(self.source_rows_hash,"source_rows_hash");require_sha256(self.cursor_hash,"cursor_hash")

@dataclass(frozen=True,slots=True)
class RelationEngineSnapshot:
    snapshot_id:str
    config_hash:str
    compiler_report_hash:str
    scan_results:tuple[RelationScanResult,...]
    candidates:tuple[RawDivergenceCandidate,...]
    health:EngineHealth
    reason_codes:tuple[str,...]
    source_revision_id:str
    created_utc_ms:int
    semantic_hash:str
    def __post_init__(self):
        _req(self.snapshot_id,"snapshot_id");require_sha256(self.config_hash,"config_hash");require_sha256(self.compiler_report_hash,"compiler_report_hash");_req(self.source_revision_id,"source_revision_id");require_sha256(self.semantic_hash,"semantic_hash")
        if self.created_utc_ms<0: raise FPI06Error("FP_HRC_SNAPSHOT_TIME_INVALID","snapshot time invalid")
        if len({c.candidate_id for c in self.candidates})!=len(self.candidates): raise FPI06Error("FP_HRC_DUPLICATE_CANDIDATE","duplicate candidate")

@dataclass(frozen=True,slots=True)
class RelationEngineCheckpoint:
    checkpoint_id:str
    checkpoint_version:str
    config_hash:str
    source_revision_id:str
    compiler_report_hash:str
    snapshot_semantic_hash:str
    payload_hash:str
    created_utc_ms:int
    def __post_init__(self):
        _req(self.checkpoint_id,"checkpoint_id");require_semver(self.checkpoint_version,"checkpoint_version");require_sha256(self.config_hash,"config_hash");_req(self.source_revision_id,"source_revision_id");require_sha256(self.compiler_report_hash,"compiler_report_hash");require_sha256(self.snapshot_semantic_hash,"snapshot_semantic_hash");require_sha256(self.payload_hash,"payload_hash")
