from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPERT = ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5"
FAST = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh"
SETUP = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh"
RULES = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh"
ENGINE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh"
TRADE_ENGINE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh"


def require(text: str, token: str, label: str) -> None:
    if token not in text:
        raise SystemExit(f"FAIL {label}: missing {token}")
    print(f"PASS {label}")


def forbid(text: str, token: str, label: str) -> None:
    if token in text:
        raise SystemExit(f"FAIL {label}: forbidden {token}")
    print(f"PASS {label}")


def main() -> None:
    expert = EXPERT.read_text(encoding="utf-8")
    fast = FAST.read_text(encoding="utf-8")
    setup = SETUP.read_text(encoding="utf-8")
    rules = RULES.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8")
    trade_engine = TRADE_ENGINE.read_text(encoding="utf-8")
    runtime = "\n".join((expert, fast, setup, rules, engine, trade_engine))

    require(expert, "FP_NDSF2WaistBacktestEngine.mqh", "dedicated_expert")
    require(expert, "cfg.scan_hooks = false", "hook_scan_disabled")
    require(expert, "cfg.scan_f1 = true", "f1_reuse")
    require(expert, "cfg.scan_f2 = true", "f2_reuse")
    require(expert, "cfg.scan_f3 = false", "f3_disabled")
    require(fast, "FP_BuildCanonicalNodesForScale", "canonical_node_reuse")
    require(fast, "FP_TryBuildFlagChainsFromOrigins", "canonical_f1_f2_reuse")
    forbid(fast, "FP_DetectScale(", "skip_general_heavy_detector")
    forbid(fast, "FP_BuildHookBranches", "skip_hook_build")
    forbid(fast, "FP_DetectAllScales", "skip_global_postprocessing")

    require(setup, "f2.f2_body_complete", "complete_unconfirmed_f2_gate")
    require(setup, "f2.status == FP_STATUS_CONFIRMED", "reject_confirmed_f2")
    require(setup, "FP_CanonicalFindParentIndex", "canonical_parent_f1")
    require(setup, "events[i].leg2", "leg2_observable_bar_freshness")
    require(setup, "f2.waist.price - entry_offset", "bullish_below_f2_waist")
    require(setup, "f2.waist.price + entry_offset", "bearish_above_f2_waist")
    require(setup, "f1.waist.price - stop_offset", "bullish_behind_f1_waist")
    require(setup, "f1.waist.price + stop_offset", "bearish_behind_f1_waist")
    require(setup, "f2.leg2.price", "f2_leg2_target")
    require(setup, "setup.reward_risk = setup.reward_distance / setup.risk_distance", "reward_risk_filter")

    require(rules, "TRADE_ACTION_PENDING", "real_pending_request")
    require(rules, "ORDER_TYPE_BUY_LIMIT", "buy_limit")
    require(rules, "ORDER_TYPE_SELL_LIMIT", "sell_limit")
    require(rules, "request.sl = setup.stop_price", "attached_stop")
    require(rules, "request.tp = setup.initial_broker_take_profit_price", "mode_aware_attached_target")
    require(rules, "OrderCheck", "broker_preflight")
    require(rules, "OrderSend", "broker_send")
    require(rules, "TRADE_ACTION_REMOVE", "stale_pending_removal")
    require(rules, "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING", "hedging_account_boundary")
    require(rules, "allow_same_direction_multiple_contexts", "same_direction_parallel_contexts")
    require(rules, "allow_opposite_direction_hedge", "opposite_direction_hedge")
    require(trade_engine, "FP_NDSF2CollectWaistBreakPairs", "parallel_context_collection")
    require(trade_engine, "FP_NDSF2ExposurePolicyAllows", "parallel_exposure_policy")
    require(engine, "FP_NDSF2CancelConsumedPendingOrders", "multi_pending_target_consumption")
    require(engine, "FP_DetectF2ExecutionScales", "fast_detector")

    forbid(runtime, "Print(", "no_runtime_print")
    forbid(runtime, "PrintFormat(", "no_runtime_printformat")
    forbid(expert, "ObjectCreate", "no_rendering")
    forbid(expert, "ChartRedraw", "no_chart_redraw")
    forbid(expert, "FileOpen", "no_csv")
    forbid(expert, "OnTimer", "no_timer")
    forbid(expert, "OnChartEvent", "no_chart_event")
    forbid(expert, "FP_RunHookPhase02DetectionCore", "no_hook_phase02")
    forbid(expert, "FP_NDSAI", "no_ai_runtime")
    forbid(rules, "GlobalVariable", "no_terminal_registry_io")
    forbid(engine, "GetMicrosecondCount", "no_timing_overhead")

    print("NDS F2 waist-break Point-2 fast backtest contract: PASS")


if __name__ == "__main__":
    main()
