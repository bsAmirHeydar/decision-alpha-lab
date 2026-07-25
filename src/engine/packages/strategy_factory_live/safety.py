from __future__ import annotations
from dataclasses import dataclass
from .models import *
from .enums import *

@dataclass
class KillSwitch:
    state: KillSwitchState = KillSwitchState.ENGAGED
    reason: str = "startup-default"
    changed_at_utc_msc: int = 0
    def engage(self, reason: str, now_utc_msc: int) -> None:
        self.state=KillSwitchState.ENGAGED; self.reason=reason or "operator"; self.changed_at_utc_msc=now_utc_msc
    def disarm(self, authorization: LiveAuthorization, now_utc_msc: int) -> bool:
        authorization.validate()
        if authorization.mode!=LiveMode.MICRO_LIVE or now_utc_msc>authorization.expires_at_utc_msc: return False
        self.state=KillSwitchState.DISARMED; self.reason="authorized"; self.changed_at_utc_msc=now_utc_msc; return True
    @property
    def engaged(self) -> bool: return self.state==KillSwitchState.ENGAGED

@dataclass
class CircuitBreaker:
    maximum_consecutive_failures: int
    cooldown_milliseconds: int
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    opened_at_utc_msc: int = 0
    last_failure_reason: str = ""
    def record_success(self) -> None:
        self.consecutive_failures=0
        if self.state==CircuitState.HALF_OPEN: self.state=CircuitState.CLOSED
    def record_failure(self, reason: str, now_utc_msc: int) -> bool:
        self.consecutive_failures+=1; self.last_failure_reason=reason
        if self.consecutive_failures>=self.maximum_consecutive_failures:
            self.state=CircuitState.OPEN; self.opened_at_utc_msc=now_utc_msc; return True
        return False
    def can_attempt(self, now_utc_msc: int) -> bool:
        if self.state==CircuitState.CLOSED: return True
        if self.state==CircuitState.OPEN and now_utc_msc-self.opened_at_utc_msc>=self.cooldown_milliseconds:
            self.state=CircuitState.HALF_OPEN; return True
        return self.state==CircuitState.HALF_OPEN
    def reset(self) -> None:
        self.state=CircuitState.CLOSED; self.consecutive_failures=0; self.opened_at_utc_msc=0; self.last_failure_reason=""

def preflight_reason(*, mode: LiveMode, intent: ExecutionIntentRecord, release: MicroLiveRelease,
        authorization: LiveAuthorization, policy: LiveSafetyPolicy, account: AccountGuardSnapshot,
        quote: QuoteSnapshot, now_utc_msc: int, session_orders: int, kill_switch: KillSwitch,
        circuit: CircuitBreaker) -> LiveRejectReason:
    if mode==LiveMode.DISABLED: return LiveRejectReason.MODE_DISABLED
    if mode==LiveMode.MICRO_LIVE and kill_switch.engaged: return LiveRejectReason.KILL_SWITCH_ENGAGED
    if not circuit.can_attempt(now_utc_msc): return LiveRejectReason.CIRCUIT_OPEN
    try:
        intent.validate(); release.validate(); authorization.validate(); policy.validate(); account.validate(); quote.validate()
    except ValueError:
        return LiveRejectReason.INVALID_INTENT
    if not intent.paper_eligible: return LiveRejectReason.INTENT_NOT_PAPER_ELIGIBLE
    if now_utc_msc>intent.expires_at_utc_msc: return LiveRejectReason.INTENT_EXPIRED
    if now_utc_msc<release.valid_from_utc_msc or now_utc_msc>release.valid_until_utc_msc: return LiveRejectReason.RELEASE_MISMATCH
    if now_utc_msc>authorization.expires_at_utc_msc: return LiveRejectReason.AUTHORIZATION_EXPIRED
    if authorization.mode!=mode or authorization.release_hash!=release.derived_hash(): return LiveRejectReason.AUTHORIZATION_INVALID
    if release.account_login!=account.account_login or authorization.account_login!=account.account_login: return LiveRejectReason.ACCOUNT_MISMATCH
    if release.account_server!=account.account_server or authorization.account_server!=account.account_server: return LiveRejectReason.SERVER_MISMATCH
    if intent.symbol!=quote.symbol or intent.symbol not in release.allowed_symbols or intent.symbol!=authorization.allowed_symbol: return LiveRejectReason.SYMBOL_NOT_ALLOWED
    if intent.strategy_id!=release.strategy_id or intent.strategy_version!=release.strategy_version: return LiveRejectReason.RELEASE_MISMATCH
    if intent.runtime_generation_id!=release.runtime_generation_id or intent.model_release_hash!=release.model_release_hash: return LiveRejectReason.RELEASE_MISMATCH
    if intent.decision_policy_hash!=release.decision_policy_hash or intent.risk_policy_hash!=release.risk_policy_hash or intent.allocation_policy_hash!=release.allocation_policy_hash: return LiveRejectReason.RELEASE_MISMATCH
    if policy.require_terminal_trade_permission and not (account.terminal_trade_allowed and account.expert_trade_allowed): return LiveRejectReason.TERMINAL_TRADE_DISABLED
    if policy.require_account_trade_permission and not account.account_trade_allowed: return LiveRejectReason.ACCOUNT_TRADE_DISABLED
    if now_utc_msc-account.snapshot_time_utc_msc>policy.maximum_account_snapshot_age_milliseconds: return LiveRejectReason.STALE_ACCOUNT_SNAPSHOT
    if now_utc_msc-quote.time_utc_msc>policy.maximum_quote_age_milliseconds: return LiveRejectReason.STALE_QUOTE
    if quote.spread_points>policy.maximum_spread_points: return LiveRejectReason.SPREAD_LIMIT
    maximum_volume=min(policy.maximum_volume_per_order,release.max_volume_per_order,authorization.maximum_volume)
    if intent.volume>maximum_volume+1e-12: return LiveRejectReason.VOLUME_LIMIT
    if intent.expected_max_loss_cash>policy.maximum_cash_risk_per_order+1e-9: return LiveRejectReason.RISK_LIMIT
    if -account.daily_realized_pnl_cash>=policy.maximum_daily_realized_loss_cash: return LiveRejectReason.DAILY_LOSS_LIMIT
    if -(account.daily_realized_pnl_cash+account.floating_pnl_cash)>=policy.maximum_daily_total_loss_cash: return LiveRejectReason.DAILY_LOSS_LIMIT
    if account.equity_cash<policy.minimum_equity_cash: return LiveRejectReason.EQUITY_FLOOR
    if account.free_margin_cash<policy.minimum_free_margin_cash: return LiveRejectReason.FREE_MARGIN_FLOOR
    if account.margin_level_percent<policy.minimum_margin_level_percent: return LiveRejectReason.MARGIN_LEVEL_FLOOR
    if account.total_exposure_volume+intent.volume>policy.maximum_total_exposure_volume+1e-12: return LiveRejectReason.EXPOSURE_LIMIT
    if session_orders>=min(policy.maximum_orders_per_session,release.max_orders_per_session,authorization.maximum_orders): return LiveRejectReason.SESSION_ORDER_LIMIT
    if account.active_order_count>=policy.maximum_concurrent_orders: return LiveRejectReason.CONCURRENT_ORDER_LIMIT
    if account.open_position_count>=policy.maximum_positions: return LiveRejectReason.POSITION_LIMIT
    return LiveRejectReason.NONE
