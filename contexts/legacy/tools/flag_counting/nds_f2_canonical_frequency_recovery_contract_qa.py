from __future__ import annotations
from tools.repository_paths import find_repository_root

import sys
from pathlib import Path

ROOT = find_repository_root(__file__)
FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "adapter": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2CanonicalPoint2SetupAdapter.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "backtest": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "phase": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2HigherTimeframePhaseFilter.mqh",
    "doc": ROOT / "docs/contexts/legacy/nds/entry/f2_waist_break_point2_limit/17_canonical_frequency_recovery_and_lifecycle.md",
    "obsidian": ROOT / "docs/history/obsidian/hook/08_entry_execution/NDS F2 Canonical Frequency Recovery and Multi-Count HTF Gate.md",
}


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"missing {label}: {token}")


def forbid(text: str, token: str, label: str, errors: list[str]) -> None:
    if token in text:
        errors.append(f"forbidden {label}: {token}")


def overlap_percent(a_entry: float, a_stop: float, b_entry: float, b_stop: float) -> float:
    a0, a1 = sorted((a_entry, a_stop))
    b0, b1 = sorted((b_entry, b_stop))
    intersection = max(0.0, min(a1, b1) - max(a0, b0))
    narrower = min(a1 - a0, b1 - b0)
    return 0.0 if narrower <= 0 else intersection / narrower * 100.0


def aggregate_direction(bull: int, bear: int) -> int:
    if bull > 0 and bear == 0:
        return 1
    if bear > 0 and bull == 0:
        return -1
    return 0


def main() -> int:
    errors: list[str] = []
    content: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        content[name] = path.read_text(encoding="utf-8")
    if errors:
        print("NDS F2 canonical frequency recovery QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    setup = content["setup"]
    adapter = content["adapter"]
    rules = content["rules"]
    backtest = content["backtest"]
    phase = content["phase"]
    doc = content["doc"]

    require(expert, '#property version   "2.10"', "expert version", errors)
    require(types, "NDS-F2-WAIST-BREAK-12", "contract version", errors)
    require(types, "nds_f2_waist_break_point2_v12", "schema version", errors)
    require(expert, "InpF2BTMaxSetupAgeBars = -1", "lifecycle-owned age default", errors)
    require(types, "cfg.max_setup_age_bars = -1", "config age default", errors)
    require(expert, "InpF2BTConsumeAttemptOnlyOnFill = true", "consume-on-fill default", errors)
    require(expert, "InpF2BTEnableFunnelDiagnostics = false", "diagnostics default-off", errors)
    require(expert, "InpF2BTRequireHedgingAccountForParallelContexts = true", "hedging fail-fast default", errors)
    require(expert, "return INIT_PARAMETERS_INCORRECT", "hedging init failure", errors)

    require(setup, "FP_NDSF2LevelTouchedSinceAvailability", "causal missed-entry check", errors)
    require(setup, "setup.target_price", "target-consumption check", errors)
    require(setup, "setup.entry_price", "entry-consumption check", errors)
    require(expert, "InpF2BTRequireCanonicalF3SpawnForLocalExit = true", "explicit local-F3 spawn input", errors)
    require(types, "require_canonical_f3_spawn_for_local_exit", "explicit local-F3 spawn config", errors)
    require(adapter, "cfg.require_canonical_f3_spawn_for_local_exit", "explicit local-F3 spawn gate", errors)

    require(rules, "FP_NDSF2ActiveAttempt", "active attempt registry", errors)
    require(rules, "TRADE_TRANSACTION_DEAL_ADD", "fill transaction", errors)
    require(rules, "TRADE_TRANSACTION_ORDER_DELETE", "terminal order transaction", errors)
    require(rules, "ORDER_STATE_CANCELED", "cancel release", errors)
    require(rules, "FP_NDSF2ReleaseActiveAttempt", "attempt release", errors)
    require(rules, "FP_NDSF2RegisterActiveAttempt", "attempt registration", errors)
    require(rules, "if(!cfg.enable_funnel_diagnostics) return;", "funnel opt-in", errors)
    forbid(rules, "Print(", "runtime Print", errors)
    forbid(rules, "PrintFormat(", "runtime PrintFormat", errors)

    require(backtest, "cfg.requested_bars = 800", "FAST history", errors)
    require(backtest, "cfg.scale_l4 = 8", "FAST L8 coverage", errors)
    require(backtest, "cfg.max_events = 1800", "FAST event cap", errors)

    require(phase, 'NDS-F2-HTF-F-PHASE-03', "phase module version", errors)
    require(phase, "FP_NDSF2HTFEvaluateCount", "per-count evaluation", errors)
    require(phase, "FP_NDSF2HTFHookOwnerRootIndex", "count-local Hook ownership", errors)
    require(phase, "qualifying_bullish_count", "bullish aggregation", errors)
    require(phase, "qualifying_bearish_count", "bearish aggregation", errors)
    require(phase, "opposite_direction_qualifying_higher_timeframe_counts", "opposite ambiguity", errors)
    require(phase, "e.parent_sequence_id != f1.sequence_id", "exact F2 parent sequence", errors)
    require(phase, "e.parent_event_id != f1.event_id", "exact F2 parent event", errors)
    forbid(phase, "lifecycle_can_spawn_f2", "spawn gate in F1 stabilization", errors)
    forbid(phase, "f2_can_spawn_f3", "spawn gate in F2 stabilization", errors)

    require(doc, "F2 validity is lifecycle-owned", "lifecycle documentation", errors)
    require(doc, "Multi-count HTF gate", "multi-count documentation", errors)
    require(content["obsidian"], "Evaluate every canonical HTF count independently", "Obsidian summary", errors)

    if aggregate_direction(2, 0) != 1:
        errors.append("reference aggregate failed: bullish-only")
    if aggregate_direction(0, 3) != -1:
        errors.append("reference aggregate failed: bearish-only")
    if aggregate_direction(1, 1) != 0:
        errors.append("reference aggregate failed: opposite ambiguity")
    if aggregate_direction(0, 0) != 0:
        errors.append("reference aggregate failed: no qualifying count")

    if round(overlap_percent(100, 80, 96, 82), 6) != 100.0:
        errors.append("reference overlap failed: nested corridor")
    if overlap_percent(100, 80, 70, 50) != 0.0:
        errors.append("reference overlap failed: disjoint corridor")

    if errors:
        print("NDS F2 canonical frequency recovery QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 canonical frequency recovery QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
