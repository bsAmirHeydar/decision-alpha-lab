from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol
import math
from .enums import *
from .hashing import stable_id, cfloat, cbool


def _safe(value: str, name: str, limit: int = 160) -> None:
    if not value or len(value) > limit or "|" in value or any(ord(c) < 32 for c in value):
        raise ValueError(f"invalid {name}")

def _finite(value: float, name: str) -> None:
    if not math.isfinite(value): raise ValueError(f"non-finite {name}")

def _positive(value: float, name: str) -> None:
    _finite(value,name)
    if value <= 0: raise ValueError(f"non-positive {name}")

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
    created_at_utc_msc: int
    expires_at_utc_msc: int
    paper_eligible: bool = True

    def validate(self) -> None:
        for value,name in ((self.intent_id,"intent_id"),(self.intent_hash,"intent_hash"),(self.batch_id,"batch_id"),
                           (self.candidate_id,"candidate_id"),(self.candidate_hash,"candidate_hash"),
                           (self.context_frame_id,"context_frame_id"),(self.strategy_id,"strategy_id"),
                           (self.strategy_version,"strategy_version"),(self.symbol,"symbol"),(self.group_id,"group_id"),
                           (self.model_release_hash,"model_release_hash"),(self.decision_policy_hash,"decision_policy_hash"),
                           (self.risk_policy_hash,"risk_policy_hash"),(self.allocation_policy_hash,"allocation_policy_hash")):
            _safe(value,name)
        if self.direction not in (-1,1): raise ValueError("invalid direction")
        for value,name in ((self.entry_price,"entry_price"),(self.stop_price,"stop_price"),(self.volume,"volume"),
                           (self.risk_budget_cash,"risk_budget_cash"),(self.expected_max_loss_cash,"expected_max_loss_cash")):
            _positive(value,name)
        if self.has_target: _positive(self.target_price,"target_price")
        if self.direction==1 and self.stop_price>=self.entry_price: raise ValueError("long stop geometry")
        if self.direction==-1 and self.stop_price<=self.entry_price: raise ValueError("short stop geometry")
        if self.expected_max_loss_cash>self.risk_budget_cash+1e-9: raise ValueError("risk exceeds budget")
        if self.created_at_utc_msc<=0 or self.expires_at_utc_msc<self.created_at_utc_msc: raise ValueError("invalid intent time")

@dataclass(frozen=True)
class MicroLiveRelease:
    release_id: str
    release_version: str
    strategy_id: str
    strategy_version: str
    runtime_generation_id: int
    model_release_hash: str
    decision_policy_hash: str
    risk_policy_hash: str
    allocation_policy_hash: str
    execution_policy_hash: str
    account_login: int
    account_server: str
    allowed_symbols: tuple[str,...]
    max_volume_per_order: float
    max_orders_per_session: int
    valid_from_utc_msc: int
    valid_until_utc_msc: int
    phase17_soak_evidence_hash: str
    reconciliation_evidence_hash: str
    anti_overfit_evidence_hash: str
    release_hash: str = ""

    def canonical(self) -> str:
        return "|".join((self.release_id,self.release_version,self.strategy_id,self.strategy_version,
            str(self.runtime_generation_id),self.model_release_hash,self.decision_policy_hash,self.risk_policy_hash,
            self.allocation_policy_hash,self.execution_policy_hash,str(self.account_login),self.account_server,
            ",".join(sorted(self.allowed_symbols)),cfloat(self.max_volume_per_order),str(self.max_orders_per_session),
            str(self.valid_from_utc_msc),str(self.valid_until_utc_msc),self.phase17_soak_evidence_hash,
            self.reconciliation_evidence_hash,self.anti_overfit_evidence_hash))
    def derived_hash(self) -> str: return stable_id("lrel",self.canonical())
    def validate(self) -> None:
        for value,name in ((self.release_id,"release_id"),(self.release_version,"release_version"),
            (self.strategy_id,"strategy_id"),(self.strategy_version,"strategy_version"),
            (self.model_release_hash,"model_release_hash"),(self.decision_policy_hash,"decision_policy_hash"),
            (self.risk_policy_hash,"risk_policy_hash"),(self.allocation_policy_hash,"allocation_policy_hash"),
            (self.execution_policy_hash,"execution_policy_hash"),(self.account_server,"account_server"),
            (self.phase17_soak_evidence_hash,"phase17_soak_evidence_hash"),
            (self.reconciliation_evidence_hash,"reconciliation_evidence_hash"),
            (self.anti_overfit_evidence_hash,"anti_overfit_evidence_hash")):
            _safe(value,name)
        if self.account_login<=0 or self.runtime_generation_id<0: raise ValueError("invalid release identity")
        if not self.allowed_symbols or len(set(self.allowed_symbols))!=len(self.allowed_symbols): raise ValueError("invalid symbols")
        for symbol in self.allowed_symbols: _safe(symbol,"allowed_symbol",64)
        _positive(self.max_volume_per_order,"max_volume_per_order")
        if self.max_orders_per_session<=0 or self.valid_until_utc_msc<=self.valid_from_utc_msc: raise ValueError("invalid release bounds")
        if self.release_hash and self.release_hash!=self.derived_hash(): raise ValueError("release hash mismatch")

@dataclass(frozen=True)
class LiveAuthorization:
    authorization_id: str
    release_hash: str
    account_login: int
    account_server: str
    allowed_symbol: str
    mode: LiveMode
    issued_at_utc_msc: int
    expires_at_utc_msc: int
    maximum_volume: float
    maximum_orders: int
    nonce: str
    operator_token_hash: str
    authorization_hash: str = ""

    def canonical(self) -> str:
        return "|".join((self.authorization_id,self.release_hash,str(self.account_login),self.account_server,
            self.allowed_symbol,str(int(self.mode)),str(self.issued_at_utc_msc),str(self.expires_at_utc_msc),
            cfloat(self.maximum_volume),str(self.maximum_orders),self.nonce,self.operator_token_hash))
    def derived_hash(self) -> str: return stable_id("lauth",self.canonical())
    def validate(self) -> None:
        for value,name in ((self.authorization_id,"authorization_id"),(self.release_hash,"release_hash"),
            (self.account_server,"account_server"),(self.allowed_symbol,"allowed_symbol"),(self.nonce,"nonce"),
            (self.operator_token_hash,"operator_token_hash")): _safe(value,name)
        if self.mode not in (LiveMode.DRY_RUN,LiveMode.MICRO_LIVE): raise ValueError("invalid live mode")
        if self.account_login<=0 or self.expires_at_utc_msc<=self.issued_at_utc_msc: raise ValueError("invalid auth bounds")
        _positive(self.maximum_volume,"maximum_volume")
        if self.maximum_orders<=0: raise ValueError("invalid maximum orders")
        if self.authorization_hash and self.authorization_hash!=self.derived_hash(): raise ValueError("authorization hash mismatch")

@dataclass(frozen=True)
class LiveSafetyPolicy:
    policy_id: str
    policy_version: str
    maximum_orders_per_session: int
    maximum_concurrent_orders: int
    maximum_positions: int
    maximum_volume_per_order: float
    maximum_total_exposure_volume: float
    maximum_cash_risk_per_order: float
    maximum_daily_realized_loss_cash: float
    maximum_daily_total_loss_cash: float
    minimum_equity_cash: float
    minimum_free_margin_cash: float
    minimum_margin_level_percent: float
    maximum_spread_points: float
    maximum_quote_age_milliseconds: int
    maximum_account_snapshot_age_milliseconds: int
    maximum_deviation_points: int
    maximum_consecutive_failures: int
    cooldown_after_failure_milliseconds: int
    one_shot_authorization: bool
    require_terminal_trade_permission: bool
    require_account_trade_permission: bool
    allow_emergency_flatten: bool
    policy_hash: str = ""

    def canonical(self) -> str:
        return "|".join((self.policy_id,self.policy_version,str(self.maximum_orders_per_session),
            str(self.maximum_concurrent_orders),str(self.maximum_positions),cfloat(self.maximum_volume_per_order),
            cfloat(self.maximum_total_exposure_volume),cfloat(self.maximum_cash_risk_per_order),
            cfloat(self.maximum_daily_realized_loss_cash),cfloat(self.maximum_daily_total_loss_cash),
            cfloat(self.minimum_equity_cash),cfloat(self.minimum_free_margin_cash),cfloat(self.minimum_margin_level_percent),
            cfloat(self.maximum_spread_points),str(self.maximum_quote_age_milliseconds),
            str(self.maximum_account_snapshot_age_milliseconds),str(self.maximum_deviation_points),
            str(self.maximum_consecutive_failures),str(self.cooldown_after_failure_milliseconds),
            cbool(self.one_shot_authorization),cbool(self.require_terminal_trade_permission),
            cbool(self.require_account_trade_permission),cbool(self.allow_emergency_flatten)))
    def derived_hash(self) -> str: return stable_id("lpol",self.canonical())
    def validate(self) -> None:
        _safe(self.policy_id,"policy_id"); _safe(self.policy_version,"policy_version")
        for value,name in ((self.maximum_volume_per_order,"maximum_volume_per_order"),
            (self.maximum_total_exposure_volume,"maximum_total_exposure_volume"),
            (self.maximum_cash_risk_per_order,"maximum_cash_risk_per_order"),
            (self.maximum_daily_realized_loss_cash,"maximum_daily_realized_loss_cash"),
            (self.maximum_daily_total_loss_cash,"maximum_daily_total_loss_cash"),
            (self.minimum_equity_cash,"minimum_equity_cash"),(self.minimum_free_margin_cash,"minimum_free_margin_cash"),
            (self.minimum_margin_level_percent,"minimum_margin_level_percent"),(self.maximum_spread_points,"maximum_spread_points")):
            _finite(value,name)
            if value<0: raise ValueError(f"negative {name}")
        for value,name in ((self.maximum_orders_per_session,"maximum_orders_per_session"),
            (self.maximum_concurrent_orders,"maximum_concurrent_orders"),(self.maximum_positions,"maximum_positions"),
            (self.maximum_quote_age_milliseconds,"maximum_quote_age_milliseconds"),
            (self.maximum_account_snapshot_age_milliseconds,"maximum_account_snapshot_age_milliseconds"),
            (self.maximum_deviation_points,"maximum_deviation_points"),(self.maximum_consecutive_failures,"maximum_consecutive_failures"),
            (self.cooldown_after_failure_milliseconds,"cooldown_after_failure_milliseconds")):
            if value<0: raise ValueError(f"negative {name}")
        if self.maximum_orders_per_session==0 or self.maximum_consecutive_failures==0: raise ValueError("zero safety bound")
        if self.policy_hash and self.policy_hash!=self.derived_hash(): raise ValueError("policy hash mismatch")

@dataclass(frozen=True)
class AccountGuardSnapshot:
    account_login: int
    account_server: str
    equity_cash: float
    balance_cash: float
    free_margin_cash: float
    margin_level_percent: float
    daily_realized_pnl_cash: float
    floating_pnl_cash: float
    total_exposure_volume: float
    active_order_count: int
    open_position_count: int
    terminal_trade_allowed: bool
    account_trade_allowed: bool
    expert_trade_allowed: bool
    snapshot_time_utc_msc: int
    snapshot_hash: str = ""
    def canonical(self) -> str:
        return "|".join((str(self.account_login),self.account_server,cfloat(self.equity_cash),cfloat(self.balance_cash),
            cfloat(self.free_margin_cash),cfloat(self.margin_level_percent),cfloat(self.daily_realized_pnl_cash),
            cfloat(self.floating_pnl_cash),cfloat(self.total_exposure_volume),str(self.active_order_count),
            str(self.open_position_count),cbool(self.terminal_trade_allowed),cbool(self.account_trade_allowed),
            cbool(self.expert_trade_allowed),str(self.snapshot_time_utc_msc)))
    def derived_hash(self) -> str: return stable_id("acct",self.canonical())
    def validate(self) -> None:
        if self.account_login<=0: raise ValueError("invalid login")
        _safe(self.account_server,"account_server")
        for value,name in ((self.equity_cash,"equity"),(self.balance_cash,"balance"),(self.free_margin_cash,"free_margin"),
                           (self.margin_level_percent,"margin_level"),(self.daily_realized_pnl_cash,"daily_realized"),
                           (self.floating_pnl_cash,"floating"),(self.total_exposure_volume,"exposure")): _finite(value,name)
        if self.equity_cash<0 or self.balance_cash<0 or self.free_margin_cash<0 or self.margin_level_percent<0 or self.total_exposure_volume<0: raise ValueError("negative account field")
        if self.active_order_count<0 or self.open_position_count<0 or self.snapshot_time_utc_msc<=0: raise ValueError("invalid account counts/time")
        if self.snapshot_hash and self.snapshot_hash!=self.derived_hash(): raise ValueError("account hash mismatch")

@dataclass(frozen=True)
class QuoteSnapshot:
    symbol: str
    bid: float
    ask: float
    point: float
    time_utc_msc: int
    sequence: int
    def validate(self) -> None:
        _safe(self.symbol,"symbol",64); _positive(self.bid,"bid"); _positive(self.ask,"ask"); _positive(self.point,"point")
        if self.ask<self.bid or self.time_utc_msc<=0 or self.sequence<0: raise ValueError("invalid quote")
    @property
    def spread_points(self) -> float: return (self.ask-self.bid)/self.point

@dataclass(frozen=True)
class NormalizedBrokerRequest:
    request_id: str
    intent_id: str
    intent_hash: str
    action: BrokerAction
    symbol: str
    direction: int
    order_kind: OrderKind
    volume: float
    price: float
    stop_price: float
    target_price: float
    has_target: bool
    deviation_points: int
    magic_number: int
    expires_at_utc_msc: int
    request_hash: str

@dataclass(frozen=True)
class BrokerCheckResult:
    request_id: str
    api_ok: bool
    retcode: int
    retcode_class: RetcodeClass
    balance_cash: float
    equity_cash: float
    margin_cash: float
    free_margin_cash: float
    comment: str
    checked_at_utc_msc: int
    result_hash: str

@dataclass(frozen=True)
class BrokerSendResult:
    request_id: str
    api_ok: bool
    retcode: int
    retcode_class: RetcodeClass
    order_ticket: int
    deal_ticket: int
    volume: float
    price: float
    bid: float
    ask: float
    comment: str
    sent_at_utc_msc: int
    result_hash: str

@dataclass(frozen=True)
class LiveDecisionRecord:
    decision_id: str
    intent_id: str
    decision: LiveDecision
    reject_reason: LiveRejectReason
    request_id: str
    authorization_id: str
    release_hash: str
    event_time_utc_msc: int
    message: str
    decision_hash: str

@dataclass(frozen=True)
class LiveTransactionRecord:
    transaction_id: str
    sequence: int
    transaction_type: LiveTransactionType
    entity_id: str
    event_time_utc_msc: int
    previous_chain_hash: str
    payload_hash: str
    chain_hash: str
    message: str

@dataclass(frozen=True)
class LiveExecutionReport:
    report_id: str
    run_id: str
    mode: LiveMode
    intents_received: int
    preflight_passed: int
    rejected: int
    checks_accepted: int
    sends_attempted: int
    sends_accepted: int
    session_orders: int
    consecutive_failures: int
    circuit_state: CircuitState
    kill_switch_state: KillSwitchState
    ledger_tail_hash: str
    generated_at_utc_msc: int
    report_hash: str

class BrokerPort(Protocol):
    def check(self, request: NormalizedBrokerRequest, now_utc_msc: int) -> BrokerCheckResult: ...
    def send(self, request: NormalizedBrokerRequest, now_utc_msc: int) -> BrokerSendResult: ...
