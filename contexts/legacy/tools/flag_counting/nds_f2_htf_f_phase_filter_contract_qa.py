from __future__ import annotations
from tools.repository_paths import find_repository_root

import sys
from pathlib import Path

ROOT = find_repository_root(__file__)
FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "phase": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2HigherTimeframePhaseFilter.mqh",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "backtest": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/contexts/legacy/nds/entry/f2_waist_break_point2_limit/13_higher_timeframe_f_phase_direction_filter.md",
    "obsidian": ROOT / "docs/history/obsidian/hook/08_entry_execution/NDS F2 Higher-Timeframe F-Phase Filter.md",
}


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"missing {label}: {token}")


def forbid(text: str, token: str, label: str, errors: list[str]) -> None:
    if token in text:
        errors.append(f"forbidden {label}: {token}")


def main() -> int:
    errors: list[str] = []
    content: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        content[name] = path.read_text(encoding="utf-8")

    if errors:
        print("NDS F2 HTF F-phase filter contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    phase = content["phase"]
    types = content["types"]
    rules = content["rules"]
    engine = content["engine"]
    backtest = content["backtest"]
    doc = content["doc"]
    obsidian = content["obsidian"]

    require(expert, '#property version   "2.10"', "expert version", errors)
    require(expert, "InpF2BTUseHigherTimeframeFPhaseFilter = true", "enabled default", errors)
    require(expert, "InpF2BTHigherTimeframe = PERIOD_H1", "H1 default", errors)
    require(expert, "InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true", "F1-to-F2 window default", errors)
    require(expert, "InpF2BTCancelPendingWhenHigherTimeframeDisallows = true", "pending cancel default", errors)
    require(expert, "FP_LoadNDSF2HigherTimeframePhaseConfig", "HTF config loader", errors)

    require(types, "NDS-F2-WAIST-BREAK-12", "contract version", errors)
    require(types, "nds_f2_waist_break_point2_v12", "schema version", errors)
    require(types, "FP_NDS_F2_RUN_PENDING_CANCELLED_HTF_FILTER", "HTF cancellation result", errors)

    require(phase, "FP_NDS_F2_HTF_PHASE_F_BULLISH", "bullish F state", errors)
    require(phase, "FP_NDS_F2_HTF_PHASE_F_BEARISH", "bearish F state", errors)
    require(phase, "FP_NDS_F2_HTF_PHASE_HOOK_OR_ND", "Hook/ND state", errors)
    require(phase, "FP_DetectAllScales", "canonical full detector", errors)
    require(phase, "cfg.scan_hooks = true", "Hook scan", errors)
    require(phase, "cfg.scan_f1 = true", "F1 scan", errors)
    require(phase, "cfg.scan_f2 = true", "F2 scan", errors)
    require(phase, "cfg.scan_f3 = true", "F3 scan", errors)
    require(phase, "timebase_cfg.exclude_live_bar = true", "closed HTF bars", errors)
    require(phase, "FP_NDSF2HTFHookOwnerRootIndex", "same-count Hook ownership resolver", errors)
    require(phase, "FP_NDSF2HTFHookBelongsToRoot", "same-count Hook gate", errors)
    require(phase, "qualifying_bullish_count", "multi-count bullish aggregation", errors)
    require(phase, "qualifying_bearish_count", "multi-count bearish aggregation", errors)
    require(phase, "opposite_direction_qualifying_higher_timeframe_counts", "opposite-count ambiguity gate", errors)
    require(phase, "snapshot.source_open_bar_time == open_bar", "HTF cache", errors)
    require(phase, "snapshot.gate_open", "entry gate state", errors)
    require(phase, "FP_NDSF2HTFEvaluateCount", "per-count lifecycle evaluation", errors)

    require(rules, "FP_NDSF2CancelPendingOrdersOutsideDirection", "pending reconciliation", errors)
    require(rules, "direction != allowed_direction", "directional cancellation", errors)

    require(engine, "entry_direction_gate_open", "trade-core gate", errors)
    require(engine, "allowed_entry_direction", "trade-core direction", errors)
    require(engine, "events[f2_index].direction != allowed_entry_direction", "candidate direction block", errors)

    require(backtest, "FP_NDSF2RefreshHigherTimeframePhase", "phase refresh", errors)
    require(backtest, "FP_NDSF2CancelPendingOrdersOutsideDirection", "pending cancellation call", errors)
    require(backtest, "needs_dynamic_exit_detection", "open-position exit continuity", errors)
    require(backtest, "!entry_gate_open && !needs_dynamic_exit_detection", "blocked fast path", errors)

    require(doc, "Higher timeframe = H1", "documented default", errors)
    require(doc, "Higher timeframe in bullish F phase", "bullish contract", errors)
    require(doc, "Higher timeframe in bearish F phase", "bearish contract", errors)
    require(doc, "Higher timeframe in Hook/ND phase", "Hook block contract", errors)
    require(doc, "Existing positions are not force-closed", "position lifecycle", errors)
    require(doc, "F1-to-F2 confirmation-window", "window documentation", errors)
    require(obsidian, "HTF bullish F → Buy only", "Obsidian bullish summary", errors)

    runtime = "\n".join(content[name] for name in (
        "expert", "phase", "types", "engine", "backtest"
    ))
    forbid(runtime, "ObjectCreate(", "renderer", errors)
    forbid(runtime, "Print(", "runtime Print", errors)
    forbid(runtime, "PrintFormat(", "runtime PrintFormat", errors)
    forbid(rules, "Print(", "runtime Print in rules", errors)
    forbid(rules, "PrintFormat(", "runtime PrintFormat in rules", errors)
    require(rules, "if(!cfg.enable_funnel_diagnostics) return;", "diagnostics opt-in guard", errors)

    if errors:
        print("NDS F2 HTF F-phase filter contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 HTF F-phase filter contract QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
