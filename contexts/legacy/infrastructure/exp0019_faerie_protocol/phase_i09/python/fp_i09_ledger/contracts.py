from __future__ import annotations
from dataclasses import dataclass
from fp_i02_kernel.enums import RelationCode,Direction,QuotaConsumptionPolicy
from fp_i07_confirmation.contracts import ConfirmedSignal
from fp_i08_weekly.contracts import DirectionGateDecision
from fp_i08_weekly.enums import GateEligibility
from .canonical import canonical_sha256,stable_id,require_identifier,require_sha256,require_semver
from .constants import *
from .enums import *
from .errors import FPI09Error

def _req(v,n):
    if not isinstance(v,str) or not v.strip(): raise FPI09Error("FP_LDG_REQUIRED_FIELD",f"{n} required")
    return v
def _minute(v,n):
    if not isinstance(v,int) or v<0 or v%M1_MS: raise FPI09Error("FP_LDG_MINUTE_INVALID",f"{n} must be UTC M1 aligned")
    return v

@dataclass(frozen=True,slots=True)
class LedgerConfig:
    context_id:str; pair_id:str; context_epoch:str; semantic_config_hash:str
    quota_scope:str=CANONICAL_QUOTA_SCOPE; winner_policy:str=CANONICAL_WINNER_POLICY
    quota_consumption_policy:QuotaConsumptionPolicy=QuotaConsumptionPolicy.UNSET
    live_execution_enabled:bool=False; ledger_version:str=LEDGER_VERSION; arbiter_version:str=ARBITER_VERSION
    checkpoint_version:str=CHECKPOINT_VERSION; tie_break_version:str=TIE_BREAK_VERSION
    def __post_init__(self):
        require_identifier(self.context_id,"context_id"); require_identifier(self.pair_id,"pair_id"); require_identifier(self.context_epoch,"context_epoch"); require_sha256(self.semantic_config_hash,"semantic_config_hash")
        for n in ("ledger_version","arbiter_version","checkpoint_version","tie_break_version"): require_semver(getattr(self,n),n)
        if self.quota_scope!=CANONICAL_QUOTA_SCOPE: raise FPI09Error("FP_LDG_QUOTA_SCOPE_NONCANONICAL","pair-global session scope required")
        if self.winner_policy!=CANONICAL_WINNER_POLICY: raise FPI09Error("FP_LDG_WINNER_POLICY_NONCANONICAL","earliest M1 hunt policy required")
        if self.live_execution_enabled: raise FPI09Error("FP_LDG_LIVE_AUTHORITY_FORBIDDEN","FP-I09 has no live authority")
        if self.quota_consumption_policy is not QuotaConsumptionPolicy.UNSET: raise FPI09Error("FP_LDG_CONSUMPTION_POLICY_UNFROZEN","FP-DEC-012 remains open")
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class PairSessionQuotaKey:
    quota_key_id:str; context_epoch:str; trading_day_id:str; pair_id:str; owner_session_id:str; session_kind:str; key_hash:str
    def __post_init__(self):
        _req(self.quota_key_id,"quota_key_id"); require_identifier(self.context_epoch,"context_epoch"); _req(self.trading_day_id,"trading_day_id"); require_identifier(self.pair_id,"pair_id"); _req(self.owner_session_id,"owner_session_id")
        if self.session_kind not in ("A","L","N"): raise FPI09Error("FP_LDG_SESSION_KIND_INVALID","quota session must be A/L/N")
        require_sha256(self.key_hash,"key_hash")

@dataclass(frozen=True,slots=True)
class EligibilityEvidence:
    evidence_id:str; signal_id:str; relation_enabled:bool; data_ready:bool; precheck_state:PrecheckState
    gate_decision_id:str; gate_eligibility:GateEligibility; evaluated_utc_ms:int; reason_codes:tuple[str,...]; evidence_hash:str
    def __post_init__(self):
        _req(self.evidence_id,"evidence_id"); _req(self.signal_id,"signal_id"); _req(self.gate_decision_id,"gate_decision_id"); _minute(self.evaluated_utc_ms,"evaluated_utc_ms"); require_sha256(self.evidence_hash,"evidence_hash")
        if tuple(sorted(set(self.reason_codes)))!=self.reason_codes: raise FPI09Error("FP_LDG_REASON_CODES_NONCANONICAL","reason codes must be sorted unique")

@dataclass(frozen=True,slots=True)
class ArbitrationContender:
    contender_id:str; signal:ConfirmedSignal; quota_key:PairSessionQuotaKey; eligibility:EligibilityEvidence
    rank_key:tuple; contender_hash:str
    def __post_init__(self):
        _req(self.contender_id,"contender_id"); require_sha256(self.contender_hash,"contender_hash")
        if self.signal.signal_id!=self.eligibility.signal_id: raise FPI09Error("FP_LDG_SIGNAL_ELIGIBILITY_MISMATCH","signal and eligibility mismatch")
        if self.signal.owner_session_id!=self.quota_key.owner_session_id: raise FPI09Error("FP_LDG_SIGNAL_SESSION_MISMATCH","signal session and quota key mismatch")
        if len(self.rank_key)!=6: raise FPI09Error("FP_LDG_RANK_KEY_INVALID","rank key must have six fields")

@dataclass(frozen=True,slots=True)
class QuotaReservation:
    reservation_id:str; quota_key:PairSessionQuotaKey; state:ReservationState; finality:ReservationFinality
    winner_signal_id:str; winner_contender_id:str; winner_rank_key:tuple; generation:int; reserved_utc_ms:int
    consumption_policy:QuotaConsumptionPolicy; prior_reservation_id:str; reason_code:str; reservation_hash:str
    def __post_init__(self):
        _req(self.reservation_id,"reservation_id"); _req(self.winner_signal_id,"winner_signal_id"); _req(self.winner_contender_id,"winner_contender_id"); _minute(self.reserved_utc_ms,"reserved_utc_ms"); _req(self.reason_code,"reason_code"); require_sha256(self.reservation_hash,"reservation_hash")
        if self.state is not ReservationState.RESERVED: raise FPI09Error("FP_LDG_RESERVATION_STATE_INVALID","I09 only emits RESERVED")
        if self.generation<1: raise FPI09Error("FP_LDG_RESERVATION_GENERATION_INVALID","generation must be positive")
        if self.consumption_policy is not QuotaConsumptionPolicy.UNSET: raise FPI09Error("FP_LDG_CONSUMPTION_POLICY_UNFROZEN","reservation must preserve UNSET")

@dataclass(frozen=True,slots=True)
class ArbitrationDecision:
    decision_id:str; quota_key:PairSessionQuotaKey; seal_state:SessionSealState; reservation:QuotaReservation|None
    winner_signal_id:str; contender_ids:tuple[str,...]; suppressed_signal_ids:tuple[str,...]; blocked_signal_ids:tuple[str,...]
    evaluated_utc_ms:int; reason_codes:tuple[str,...]; decision_hash:str
    def __post_init__(self):
        _req(self.decision_id,"decision_id"); _minute(self.evaluated_utc_ms,"evaluated_utc_ms"); require_sha256(self.decision_hash,"decision_hash")
        if self.reservation is None and self.winner_signal_id: raise FPI09Error("FP_LDG_WINNER_WITHOUT_RESERVATION","winner requires reservation")
        if self.reservation and self.reservation.winner_signal_id!=self.winner_signal_id: raise FPI09Error("FP_LDG_RESERVATION_WINNER_MISMATCH","winner mismatch")
        all_ids=self.contender_ids+self.suppressed_signal_ids+self.blocked_signal_ids
        if len(all_ids)!=len(set(all_ids)): raise FPI09Error("FP_LDG_DECISION_SIGNAL_OVERLAP","signal appears in multiple decision sets")

@dataclass(frozen=True,slots=True)
class LedgerEvent:
    event_id:str; sequence:int; event_type:LedgerEventType; aggregate_id:str; signal_id:str; quota_key_id:str
    occurred_utc_ms:int; source_phase:str; reason_code:str; payload_hash:str; prior_event_hash:str; event_hash:str
    def __post_init__(self):
        _req(self.event_id,"event_id"); _req(self.aggregate_id,"aggregate_id"); _minute(self.occurred_utc_ms,"occurred_utc_ms"); _req(self.source_phase,"source_phase"); _req(self.reason_code,"reason_code"); require_sha256(self.payload_hash,"payload_hash"); require_sha256(self.event_hash,"event_hash")
        if self.sequence<0: raise FPI09Error("FP_LDG_EVENT_SEQUENCE_INVALID","sequence must be nonnegative")
        if self.sequence==0 and self.prior_event_hash: raise FPI09Error("FP_LDG_GENESIS_PRIOR_HASH_FORBIDDEN","genesis cannot have prior hash")
        if self.sequence>0: require_sha256(self.prior_event_hash,"prior_event_hash")

@dataclass(frozen=True,slots=True)
class SignalLedgerRecord:
    ledger_record_id:str; signal:ConfirmedSignal; gate_decision:DirectionGateDecision; eligibility:EligibilityEvidence
    disposition:LedgerDisposition; quota_key_id:str; winner_signal_id:str; reservation_id:str; reason_codes:tuple[str,...]
    first_event_sequence:int; last_event_sequence:int; record_hash:str
    def __post_init__(self):
        _req(self.ledger_record_id,"ledger_record_id"); require_sha256(self.record_hash,"record_hash")
        if self.signal.signal_id!=self.gate_decision.subject_signal_id or self.signal.signal_id!=self.eligibility.signal_id: raise FPI09Error("FP_LDG_RECORD_SIGNAL_MISMATCH","record components mismatch")
        if self.last_event_sequence<self.first_event_sequence: raise FPI09Error("FP_LDG_RECORD_SEQUENCE_INVALID","record sequence invalid")

@dataclass(frozen=True,slots=True)
class LedgerSnapshot:
    snapshot_id:str; config_hash:str; events:tuple[LedgerEvent,...]; records:tuple[SignalLedgerRecord,...]
    decisions:tuple[ArbitrationDecision,...]; reservations:tuple[QuotaReservation,...]; chain_head_hash:str
    signal_index:tuple[tuple[str,int],...]; session_index:tuple[tuple[str,tuple[str,...]],...]; relation_index:tuple[tuple[str,tuple[str,...]],...]
    health:EngineHealth; reason_codes:tuple[str,...]; created_utc_ms:int; snapshot_hash:str
    def __post_init__(self):
        _req(self.snapshot_id,"snapshot_id"); require_sha256(self.config_hash,"config_hash"); _minute(self.created_utc_ms,"created_utc_ms"); require_sha256(self.snapshot_hash,"snapshot_hash")
        if self.events: require_sha256(self.chain_head_hash,"chain_head_hash")
        if len({e.event_id for e in self.events})!=len(self.events): raise FPI09Error("FP_LDG_DUPLICATE_EVENT","duplicate event id")
        if len({r.signal.signal_id for r in self.records})!=len(self.records): raise FPI09Error("FP_LDG_DUPLICATE_SIGNAL_RECORD","duplicate signal record")

@dataclass(frozen=True,slots=True)
class LedgerCheckpoint:
    checkpoint_id:str; checkpoint_version:str; config_hash:str; chain_head_hash:str; event_count:int
    snapshot:LedgerSnapshot; source_revision_id:str; created_utc_ms:int; payload_hash:str
    def __post_init__(self):
        _req(self.checkpoint_id,"checkpoint_id"); require_semver(self.checkpoint_version,"checkpoint_version"); require_sha256(self.config_hash,"config_hash"); require_sha256(self.chain_head_hash,"chain_head_hash"); _req(self.source_revision_id,"source_revision_id"); _minute(self.created_utc_ms,"created_utc_ms"); require_sha256(self.payload_hash,"payload_hash")
        if self.event_count<0 or self.event_count!=len(self.snapshot.events): raise FPI09Error("FP_LDG_CHECKPOINT_EVENT_COUNT_INVALID","checkpoint event count mismatch")

@dataclass(frozen=True,slots=True)
class CheckpointValidation:
    validation_id:str; decision:CheckpointDecision; checkpoint_id:str; reason_code:str; expected_config_hash:str
    observed_config_hash:str; expected_chain_head_hash:str; observed_chain_head_hash:str; validation_hash:str
    def __post_init__(self):
        _req(self.validation_id,"validation_id"); _req(self.checkpoint_id,"checkpoint_id"); _req(self.reason_code,"reason_code"); require_sha256(self.expected_config_hash,"expected_config_hash"); require_sha256(self.observed_config_hash,"observed_config_hash"); require_sha256(self.validation_hash,"validation_hash")
