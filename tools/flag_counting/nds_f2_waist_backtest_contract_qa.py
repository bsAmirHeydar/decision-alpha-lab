from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPERT = ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5"
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
    rules = RULES.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8")
    trade_engine = TRADE_ENGINE.read_text(encoding="utf-8")

    require(expert, "FP_NDSF2WaistBacktestEngine.mqh", "dedicated_expert")
    require(expert, "cfg.scan_f1 = true", "f1_reuse")
    require(expert, "cfg.scan_f2 = true", "f2_reuse")
    require(expert, "cfg.scan_f3 = false", "f3_disabled")
    require(rules, "f2.f2_can_spawn_f3", "confirmed_f2_gate")
    require(rules, "FP_CanonicalFindParentIndex", "canonical_parent_f1")
    require(rules, "f2.waist.price - offset", "bullish_below_f2_waist")
    require(rules, "f2.waist.price + offset", "bearish_above_f2_waist")
    require(rules, "f1.waist.price", "f1_waist_stop")
    require(rules, "f2.leg2.price", "f2_leg2_target")
    require(rules, "BuyLimit", "buy_limit")
    require(rules, "SellLimit", "sell_limit")
    require(rules, "setup.stop_price, setup.target_price", "attached_sl_tp")
    require(trade_engine, "SINGLE_F2_LIMIT_PENDING", "single_pending")
    require(trade_engine, "POSITION_HELD_BROKER_SL_TP", "single_position")
    require(engine, "FP_NDSF2BacktestHasManagedExposure", "exposure_fast_path")
    require(engine, "FP_DetectAllScales", "canonical_detector_reuse")

    forbid(expert, "FP_RunHookPhase02DetectionCore", "no_hook_phase02")
    forbid(expert, "ObjectCreate", "no_rendering")
    forbid(expert, "ChartRedraw", "no_chart_redraw")
    forbid(expert, "FileOpen", "no_csv")
    forbid(expert, "OnTimer", "no_timer")
    forbid(expert, "OnChartEvent", "no_chart_event")
    forbid(expert, "FP_NDSAI", "no_ai_runtime")

    print("NDS F2 waist backtest contract: PASS")


if __name__ == "__main__":
    main()
