"""Hard execution-risk gates independent of strategy or model confidence."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, Mapping, Optional, Sequence

from ..contracts import ExecutionIntent


@dataclass(frozen=True)
class RiskPolicy:
    policy_id: str
    max_risk_dollars_per_intent: float
    max_daily_risk_dollars: float
    max_daily_loss_dollars: float
    max_open_risk_dollars: float
    max_strategy_open_risk_dollars: float
    max_symbol_open_risk_dollars: float
    max_concurrent_positions: int
    allowed_strategies: Sequence[str] = field(default_factory=tuple)
    allowed_symbols: Sequence[str] = field(default_factory=tuple)


@dataclass
class RiskState:
    trading_day: date
    reserved_daily_risk: float = 0.0
    realized_daily_pnl: float = 0.0
    open_risk: float = 0.0
    concurrent_positions: int = 0
    strategy_open_risk: Dict[str, float] = field(default_factory=dict)
    symbol_open_risk: Dict[str, float] = field(default_factory=dict)
    kill_switch: bool = False


@dataclass(frozen=True)
class RiskGateDecision:
    approved: bool
    reasons: Sequence[str]


def evaluate_intent(intent: ExecutionIntent, policy: RiskPolicy, state: RiskState) -> RiskGateDecision:
    intent.validate()
    reasons = []
    if state.kill_switch:
        reasons.append("kill_switch_active")
    if policy.allowed_strategies and intent.strategy_id not in policy.allowed_strategies:
        reasons.append("strategy_not_allowed")
    if policy.allowed_symbols and intent.symbol not in policy.allowed_symbols:
        reasons.append("symbol_not_allowed")
    if intent.risk_dollars > policy.max_risk_dollars_per_intent:
        reasons.append("intent_risk_limit")
    if state.reserved_daily_risk + intent.risk_dollars > policy.max_daily_risk_dollars:
        reasons.append("daily_risk_limit")
    if state.realized_daily_pnl <= -abs(policy.max_daily_loss_dollars):
        reasons.append("daily_loss_lock")
    if state.open_risk + intent.risk_dollars > policy.max_open_risk_dollars:
        reasons.append("portfolio_open_risk_limit")
    strategy_risk = state.strategy_open_risk.get(intent.strategy_id, 0.0)
    if strategy_risk + intent.risk_dollars > policy.max_strategy_open_risk_dollars:
        reasons.append("strategy_open_risk_limit")
    symbol_risk = state.symbol_open_risk.get(intent.symbol, 0.0)
    if symbol_risk + intent.risk_dollars > policy.max_symbol_open_risk_dollars:
        reasons.append("symbol_open_risk_limit")
    if state.concurrent_positions >= policy.max_concurrent_positions:
        reasons.append("concurrent_position_limit")
    return RiskGateDecision(approved=not reasons, reasons=tuple(reasons))


def reserve_intent(intent: ExecutionIntent, state: RiskState) -> None:
    state.reserved_daily_risk += intent.risk_dollars
    state.open_risk += intent.risk_dollars
    state.concurrent_positions += 1
    state.strategy_open_risk[intent.strategy_id] = state.strategy_open_risk.get(intent.strategy_id, 0.0) + intent.risk_dollars
    state.symbol_open_risk[intent.symbol] = state.symbol_open_risk.get(intent.symbol, 0.0) + intent.risk_dollars


def release_intent(intent: ExecutionIntent, state: RiskState, realized_pnl: float) -> None:
    state.open_risk = max(0.0, state.open_risk - intent.risk_dollars)
    state.concurrent_positions = max(0, state.concurrent_positions - 1)
    state.strategy_open_risk[intent.strategy_id] = max(
        0.0, state.strategy_open_risk.get(intent.strategy_id, 0.0) - intent.risk_dollars
    )
    state.symbol_open_risk[intent.symbol] = max(
        0.0, state.symbol_open_risk.get(intent.symbol, 0.0) - intent.risk_dollars
    )
    state.realized_daily_pnl += realized_pnl
