from __future__ import annotations
from dataclasses import dataclass
from .canonical import *
from .constants import *
from .enums import *
from .errors import FPI15Error

@dataclass(frozen=True,slots=True)
class DiagnosticAcceptanceProof:
    acceptance_id:str; status:str; context_id:str; pair_id:str; config_hash:str; source_revision_id:str; consensus_hash:str; accepted_utc_ms:int
    def __post_init__(self):
        for n in ("acceptance_id","context_id","pair_id","source_revision_id"): require_id(getattr(self,n),n)
        require_hash(self.config_hash,"config_hash"); require_hash(self.consensus_hash,"consensus_hash")
        if self.accepted_utc_ms<0: raise FPI15Error("FP_PAPER_ACCEPTANCE_TIME_INVALID","accepted time invalid")

@dataclass(frozen=True,slots=True)
class WinnerSignalInput:
    signal_id:str; signal_hash:str; candidate_id:str; relation:str; direction:TradeDirection; hunter_symbol:str; protected_symbol:str; owner_session_id:str; quota_key_id:str; i09_reservation_id:str; i09_reservation_finality:ReservationFinality; first_hunt_m1_utc_ms:int; confirmation_close_utc_ms:int; raw_structural_stop:float; source_revision_id:str; config_hash:str; semantic_rank_key:tuple
    def __post_init__(self):
        for n in ("signal_id","candidate_id","relation","hunter_symbol","protected_symbol","owner_session_id","quota_key_id","i09_reservation_id","source_revision_id"): require_id(getattr(self,n),n)
        require_hash(self.signal_hash,"signal_hash"); require_hash(self.config_hash,"config_hash"); require_positive(self.raw_structural_stop,"raw_structural_stop")
        if self.hunter_symbol==self.protected_symbol: raise FPI15Error("FP_PAPER_ROLE_COLLISION","hunter and protected must differ")
        if self.first_hunt_m1_utc_ms<0 or self.confirmation_close_utc_ms<self.first_hunt_m1_utc_ms: raise FPI15Error("FP_PAPER_TIME_INVALID","signal time invalid")

@dataclass(frozen=True,slots=True)
class CausalReadiness:
    watermark_utc_ms:int; primary_complete:bool; secondary_complete:bool; unresolved_gap_count:int; reservation_is_active_winner:bool; session_sealed:bool=False
    @property
    def complete(self): return self.primary_complete and self.secondary_complete and self.unresolved_gap_count==0

@dataclass(frozen=True,slots=True)
class QuoteSnapshot:
    quote_id:str; symbol:str; bid:float; ask:float; captured_utc_ms:int; source_revision_id:str
    def __post_init__(self):
        require_id(self.quote_id,"quote_id"); require_id(self.symbol,"symbol"); require_id(self.source_revision_id,"source_revision_id")
        require_positive(self.bid,"bid"); require_positive(self.ask,"ask")
        if self.ask<self.bid: raise FPI15Error("FP_PAPER_QUOTE_CROSSED","ask below bid")
        if self.captured_utc_ms<0: raise FPI15Error("FP_PAPER_QUOTE_TIME_INVALID","quote time invalid")
    @property
    def spread(self): return self.ask-self.bid
    @property
    def quote_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class SymbolSpec:
    symbol:str; tick_size:float; tick_value_loss_per_lot:float; volume_min:float; volume_max:float; volume_step:float; stops_level_price:float=0.0; freeze_level_price:float=0.0
    def __post_init__(self):
        require_id(self.symbol,"symbol")
        for n in ("tick_size","tick_value_loss_per_lot","volume_min","volume_max","volume_step"): require_positive(getattr(self,n),n)
        if self.volume_max<self.volume_min: raise FPI15Error("FP_PAPER_VOLUME_RANGE_INVALID","volume max below min")
        if self.stops_level_price<0 or self.freeze_level_price<0: raise FPI15Error("FP_PAPER_LEVEL_INVALID","broker levels cannot be negative")

@dataclass(frozen=True,slots=True)
class RiskConfig:
    fixed_risk_amount:float; target_r_multiple:float; max_slippage_price:float; round_trip_cost_per_lot:float=0.0; risk_tolerance:float=RISK_TOLERANCE
    def __post_init__(self):
        require_positive(self.fixed_risk_amount,"fixed_risk_amount"); require_positive(self.target_r_multiple,"target_r_multiple")
        if self.max_slippage_price<0 or self.round_trip_cost_per_lot<0 or self.risk_tolerance<0: raise FPI15Error("FP_PAPER_RISK_CONFIG_INVALID","risk config contains negative value")
    @property
    def config_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class AdmissionDecision:
    status:AdmissionStatus; signal_id:str; reason_codes:tuple[str,...]; decision_id:str

@dataclass(frozen=True,slots=True)
class RiskGeometry:
    geometry_id:str; status:GeometryStatus; direction:TradeDirection; symbol:str; quote_id:str; planned_entry:float; worst_case_entry:float; raw_stop:float; spread_snapshot:float; adjusted_stop:float; target:float; stop_distance:float; target_distance:float; minimum_required_distance:float; reason_codes:tuple[str,...]; geometry_hash:str

@dataclass(frozen=True,slots=True)
class SizingResult:
    sizing_id:str; status:GeometryStatus; risk_budget:float; loss_per_lot:float; raw_volume:float; volume:float; estimated_max_loss:float; risk_utilization:float; reason_codes:tuple[str,...]; sizing_hash:str

@dataclass(frozen=True,slots=True)
class ExecutionPlan:
    plan_id:str; parent_plan_id:str; revision:int; state:PlanState; signal_id:str; signal_hash:str; quota_key_id:str; i09_reservation_id:str; trade_symbol:str; direction:TradeDirection; geometry:RiskGeometry; sizing:SizingResult; risk_config_hash:str; diagnostic_acceptance_id:str; source_revision_id:str; created_utc_ms:int; reason_codes:tuple[str,...]; plan_hash:str

@dataclass(frozen=True,slots=True)
class PaperPolicyConfig:
    profile:PaperPolicyProfile; consume_event:PaperConsumeEvent; releasable_reason_codes:frozenset[str]; policy_version:str="1.0.0"
    @property
    def policy_hash(self): return sha256({"profile":self.profile,"consume":self.consume_event,"release":self.releasable_reason_codes,"version":self.policy_version})

@dataclass(frozen=True,slots=True)
class PaperQuotaRecord:
    quota_key_id:str; state:QuotaState; winner_signal_id:str=""; plan_id:str=""; paper_reservation_id:str=""; consumed_event:PaperConsumeEvent=PaperConsumeEvent.UNSET; generation:int=0; policy_hash:str=""; reason_codes:tuple[str,...]=(); record_hash:str=""

@dataclass(frozen=True,slots=True)
class PaperOrder:
    order_id:str; plan_id:str; signal_id:str; state:OrderState; requested_volume:float; filled_volume:float; average_fill_price:float; created_utc_ms:int; updated_utc_ms:int; reason_codes:tuple[str,...]; order_hash:str

@dataclass(frozen=True,slots=True)
class PaperFill:
    fill_id:str; order_id:str; volume:float; price:float; fill_utc_ms:int; fill_sequence:int; fill_hash:str

@dataclass(frozen=True,slots=True)
class PaperPosition:
    position_id:str; order_id:str; plan_id:str; symbol:str; direction:TradeDirection; volume:float; average_entry:float; stop:float; target:float; state:PositionState; opened_utc_ms:int; closed_utc_ms:int=0; close_price:float=0.0; realized_pnl:float=0.0; position_hash:str=""

@dataclass(frozen=True,slots=True)
class ReconciliationEvent:
    sequence:int; event_type:LedgerEventType; aggregate_id:str; event_utc_ms:int; payload_hash:str; prior_event_hash:str; event_id:str; event_hash:str; reason_codes:tuple[str,...]=()

@dataclass(frozen=True,slots=True)
class PaperRunResult:
    run_id:str; scenario:PaperScenario; plan:ExecutionPlan|None; quota:PaperQuotaRecord; order:PaperOrder|None; fills:tuple[PaperFill,...]; position:PaperPosition|None; ledger:tuple[ReconciliationEvent,...]; health:HealthState; reason_codes:tuple[str,...]; run_hash:str

@dataclass(frozen=True,slots=True)
class RevalidationResult:
    disposition:RevalidationDisposition; prior_plan_id:str; plan:ExecutionPlan|None; reason_codes:tuple[str,...]; result_id:str

@dataclass(frozen=True,slots=True)
class PaperCheckpoint:
    checkpoint_id:str; version:str; config_hash:str; policy_hash:str; ledger:tuple[ReconciliationEvent,...]; quota_records:tuple[PaperQuotaRecord,...]; orders:tuple[PaperOrder,...]; fills:tuple[PaperFill,...]; positions:tuple[PaperPosition,...]; payload_hash:str

@dataclass(frozen=True,slots=True)
class CheckpointValidation:
    disposition:CheckpointDisposition; reason_codes:tuple[str,...]

@dataclass(frozen=True,slots=True)
class PaperAcceptance:
    phase_id:str; source_status:AcceptanceStatus; risk_cap_status:AcceptanceStatus; sell_spread_status:AcceptanceStatus; quota_status:AcceptanceStatus; lifecycle_status:AcceptanceStatus; restart_status:AcceptanceStatus; metaeditor_status:AcceptanceStatus; local_runtime_status:AcceptanceStatus; paper_ready:bool; live_ready:bool; acceptance_hash:str
