from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
import math
from .enums import *
from .hashing import stable_id, cfloat, cbool


def _safe(value: str, name: str, limit: int = 160) -> None:
    if not value or len(value) > limit or any(ch in value for ch in "|\r\n\t"):
        raise ValueError(f"invalid {name}")


def _positive(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"invalid {name}")


@dataclass(frozen=True)
class ExecutionIntentRecord:
    intent_id: str
    intent_hash: str
    batch_id: str
    candidate_id: str
    candidate_hash: str
    context_frame_id: str
    strategy_id: str
    strategy_version: str
    symbol: str
    group_id: str
    direction: int
    runtime_generation_id: int
    model_release_hash: str
    decision_policy_hash: str
    risk_policy_hash: str
    allocation_policy_hash: str
    order_kind: OrderKind
    entry_price: float
    stop_price: float
    target_price: float
    has_target: bool
    volume: float
    risk_budget_cash: float
    expected_max_loss_cash: float
    priority: int
    created_at_utc_msc: int
    expires_at_utc_msc: int
    paper_eligible: bool

    def validate(self) -> None:
        for value,name in ((self.intent_id,"intent_id"),(self.intent_hash,"intent_hash"),(self.batch_id,"batch_id"),
                           (self.candidate_id,"candidate_id"),(self.candidate_hash,"candidate_hash"),
                           (self.context_frame_id,"context_frame_id"),(self.strategy_id,"strategy_id"),
                           (self.strategy_version,"strategy_version"),(self.symbol,"symbol"),(self.group_id,"group_id"),
                           (self.model_release_hash,"model_release_hash"),(self.decision_policy_hash,"decision_policy_hash"),
                           (self.risk_policy_hash,"risk_policy_hash"),(self.allocation_policy_hash,"allocation_policy_hash")):
            _safe(value,name)
        if self.direction not in (-1,1): raise ValueError("invalid direction")
        if self.runtime_generation_id < 0: raise ValueError("invalid runtime generation")
        if self.order_kind not in (OrderKind.MARKET,OrderKind.LIMIT,OrderKind.STOP): raise ValueError("invalid order kind")
        for value,name in ((self.entry_price,"entry_price"),(self.stop_price,"stop_price"),(self.volume,"volume"),
                           (self.risk_budget_cash,"risk_budget_cash"),(self.expected_max_loss_cash,"expected_max_loss_cash")):
            _positive(value,name)
        if self.direction == 1 and self.stop_price >= self.entry_price: raise ValueError("long stop geometry")
        if self.direction == -1 and self.stop_price <= self.entry_price: raise ValueError("short stop geometry")
        if self.has_target:
            _positive(self.target_price,"target_price")
            if self.direction == 1 and self.target_price <= self.entry_price: raise ValueError("long target geometry")
            if self.direction == -1 and self.target_price >= self.entry_price: raise ValueError("short target geometry")
        if self.expected_max_loss_cash > self.risk_budget_cash + 1e-9: raise ValueError("risk budget exceeded")
        if self.priority <= 0 or self.created_at_utc_msc <= 0 or self.expires_at_utc_msc < self.created_at_utc_msc:
            raise ValueError("invalid intent time or priority")


@dataclass(frozen=True)
class QuoteObservation:
    symbol: str
    bid: float
    ask: float
    time_utc_msc: int
    sequence: int
    source: str = "terminal"

    def validate(self) -> None:
        _safe(self.symbol,"symbol"); _safe(self.source,"source")
        _positive(self.bid,"bid"); _positive(self.ask,"ask")
        if self.ask < self.bid: raise ValueError("crossed quote")
        if self.time_utc_msc <= 0 or self.sequence < 0: raise ValueError("invalid quote identity")


@dataclass(frozen=True)
class PaperExecutionPolicy:
    policy_id: str
    policy_version: str
    mode: ExecutionMode
    point: float
    adverse_slippage_points: float
    commission_per_lot_per_side: float
    max_fill_volume_per_quote: float
    maximum_quote_age_milliseconds: int
    allow_research_only_intents: bool
    allow_partial_fills: bool
    fill_market_on_next_quote: bool
    deterministic_seed: int
    policy_hash: str = ""

    def canonical(self) -> str:
        return "|".join((self.policy_id,self.policy_version,str(int(self.mode)),cfloat(self.point),
            cfloat(self.adverse_slippage_points),cfloat(self.commission_per_lot_per_side),
            cfloat(self.max_fill_volume_per_quote),str(self.maximum_quote_age_milliseconds),
            cbool(self.allow_research_only_intents),cbool(self.allow_partial_fills),
            cbool(self.fill_market_on_next_quote),str(self.deterministic_seed)))

    def derived_hash(self) -> str: return stable_id("xpol",self.canonical())

    def validate(self) -> None:
        _safe(self.policy_id,"policy_id"); _safe(self.policy_version,"policy_version")
        _positive(self.point,"point")
        for value,name in ((self.adverse_slippage_points,"adverse_slippage_points"),
                           (self.commission_per_lot_per_side,"commission_per_lot_per_side"),
                           (self.max_fill_volume_per_quote,"max_fill_volume_per_quote")):
            if not math.isfinite(value) or value < 0.0: raise ValueError(f"invalid {name}")
        if self.maximum_quote_age_milliseconds < 0: raise ValueError("invalid maximum quote age")
        if self.policy_hash and self.policy_hash != self.derived_hash(): raise ValueError("policy hash mismatch")


@dataclass
class PaperOrder:
    order_id: str
    intent_id: str
    intent_hash: str
    symbol: str
    direction: int
    order_kind: OrderKind
    state: OrderState
    requested_volume: float
    filled_volume: float
    remaining_volume: float
    requested_price: float
    average_fill_price: float
    stop_price: float
    target_price: float
    has_target: bool
    accepted_at_utc_msc: int
    updated_at_utc_msc: int
    expires_at_utc_msc: int
    last_quote_sequence: int = -1
    reject_reason: RejectReason = RejectReason.NONE
    order_hash: str = ""

    def canonical(self) -> str:
        return "|".join((self.order_id,self.intent_id,self.intent_hash,self.symbol,str(self.direction),
            str(int(self.order_kind)),str(int(self.state)),cfloat(self.requested_volume),cfloat(self.filled_volume),
            cfloat(self.remaining_volume),cfloat(self.requested_price),cfloat(self.average_fill_price),
            cfloat(self.stop_price),cfloat(self.target_price),cbool(self.has_target),str(self.accepted_at_utc_msc),
            str(self.updated_at_utc_msc),str(self.expires_at_utc_msc),str(self.last_quote_sequence),str(int(self.reject_reason))))

    def refresh_hash(self) -> None: self.order_hash=stable_id("pord",self.canonical())


@dataclass(frozen=True)
class FillRecord:
    fill_id: str
    order_id: str
    intent_id: str
    position_id: str
    symbol: str
    direction: int
    reason: FillReason
    volume: float
    price: float
    commission_cash: float
    slippage_cash_proxy: float
    quote_sequence: int
    fill_time_utc_msc: int
    fill_hash: str


@dataclass
class PositionRecord:
    position_id: str
    intent_id: str
    symbol: str
    direction: int
    state: PositionState
    volume: float
    average_entry_price: float
    stop_price: float
    target_price: float
    has_target: bool
    opened_at_utc_msc: int
    closed_at_utc_msc: int = 0
    average_exit_price: float = 0.0
    realized_gross_price_units: float = 0.0
    commission_cash: float = 0.0
    close_reason: FillReason | None = None
    position_hash: str = ""

    def canonical(self) -> str:
        return "|".join((self.position_id,self.intent_id,self.symbol,str(self.direction),str(int(self.state)),
            cfloat(self.volume),cfloat(self.average_entry_price),cfloat(self.stop_price),cfloat(self.target_price),
            cbool(self.has_target),str(self.opened_at_utc_msc),str(self.closed_at_utc_msc),
            cfloat(self.average_exit_price),cfloat(self.realized_gross_price_units),cfloat(self.commission_cash),
            str(int(self.close_reason)) if self.close_reason is not None else "0"))

    def refresh_hash(self) -> None: self.position_hash=stable_id("ppos",self.canonical())


@dataclass(frozen=True)
class TransactionRecord:
    transaction_id: str
    sequence: int
    transaction_type: TransactionType
    entity_id: str
    event_time_utc_msc: int
    previous_chain_hash: str
    payload_hash: str
    chain_hash: str
    message: str


@dataclass(frozen=True)
class ObservedPosition:
    external_position_id: str
    symbol: str
    direction: int
    volume: float
    average_price: float
    observed_at_utc_msc: int


@dataclass(frozen=True)
class ReconciliationItem:
    key: str
    status: ReconciliationStatus
    expected_position_id: str
    observed_position_id: str
    expected_volume: float
    observed_volume: float
    expected_price: float
    observed_price: float
    message: str


@dataclass(frozen=True)
class ReconciliationReport:
    report_id: str
    report_time_utc_msc: int
    matched: int
    mismatched: int
    items: tuple[ReconciliationItem,...]
    report_hash: str


@dataclass(frozen=True)
class ShadowComparison:
    comparison_id: str
    intent_id: str
    paper_order_id: str
    observed_external_order_id: str
    paper_fill_price: float
    observed_fill_price: float
    paper_fill_time_utc_msc: int
    observed_fill_time_utc_msc: int
    price_delta: float
    latency_delta_milliseconds: int
    volume_delta: float
    matched: bool
    comparison_hash: str


@dataclass(frozen=True)
class ExecutionTelemetry:
    intents_received: int
    intents_accepted: int
    intents_rejected: int
    orders_working: int
    orders_filled: int
    orders_expired: int
    orders_canceled: int
    fills: int
    positions_open: int
    positions_closed: int
    duplicate_intents: int
    stale_quotes: int


@dataclass(frozen=True)
class ExecutionReport:
    report_id: str
    run_id: str
    mode: ExecutionMode
    policy_hash: str
    generated_at_utc_msc: int
    orders: tuple[PaperOrder,...]
    fills: tuple[FillRecord,...]
    positions: tuple[PositionRecord,...]
    transactions: tuple[TransactionRecord,...]
    telemetry: ExecutionTelemetry
    report_hash: str


@dataclass(frozen=True)
class ExecutionRunManifest:
    run_id: str
    runtime_generation_id: int
    mode: ExecutionMode
    policy_hash: str
    decision_run_id: str
    started_at_utc_msc: int
    input_ledger_hash: str
    manifest_hash: str
