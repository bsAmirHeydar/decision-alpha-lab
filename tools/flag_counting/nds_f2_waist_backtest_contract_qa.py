from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPERT = ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5"
FAST = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh"
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
    rules = RULES.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8")
    trade_engine = TRADE_ENGINE.read_text(encoding="utf-8")
    runtime = "\n".join((expert, fast, rules, engine, trade_engine))

    require(expert, "FP_NDSF2WaistBacktestEngine.mqh", "dedicated_expert")
    require(expert, "cfg.scan_hooks = false", "hook_scan_disabled")
    require(expert, "cfg.scan_f1 = true", "f1_reuse")
    require(expert, "cfg.scan_f2 = true", "f2_reuse")
    require(expert, "cfg.scan_f3 = false", "f3_disabled")
    require(fast, "FP_DetectScale", "canonical_stage_reuse")
    forbid(fast, "FP_DetectAllScales", "skip_global_postprocessing")
    require(rules, "f2.f2_can_spawn_f3", "confirmed_f2_gate")
    require(rules, "FP_CanonicalFindParentIndex", "canonical_parent_f1")
    require(rules, "FP_NDSF2NodeAvailabilityIndex", "observable_bar_freshness")
    require(rules, "f2.waist.price - offset", "bullish_below_f2_waist")
    require(rules, "f2.waist.price + offset", "bearish_above_f2_waist")
    require(rules, "f1.waist.price", "f1_waist_stop")
    require(rules, "f2.leg2.price", "f2_leg2_target")
    require(rules, "TRADE_ACTION_PENDING", "real_pending_request")
    require(rules, "ORDER_TYPE_BUY_LIMIT", "buy_limit")
    require(rules, "ORDER_TYPE_SELL_LIMIT", "sell_limit")
    require(rules, "request.sl = setup.stop_price", "attached_stop")
    require(rules, "request.tp = setup.target_price", "attached_target")
    require(rules, "OrderCheck", "broker_preflight")
    require(rules, "OrderSend", "broker_send")
    require(trade_engine, "FP_NDSF2CountManagedOrders", "single_pending")
    require(trade_engine, "FP_NDSF2CountManagedPositions", "single_position")
    require(engine, "FP_NDSF2BacktestHasManagedExposure", "exposure_fast_path")
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
    forbid(trade_engine, "AcquireEntryLock", "no_global_mutex")
    forbid(engine, "GetMicrosecondCount", "no_timing_overhead")

    print("NDS F2 waist fast backtest contract: PASS")


if __name__ == "__main__":
    main()
