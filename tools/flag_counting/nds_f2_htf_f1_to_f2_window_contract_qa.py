from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "phase": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2HigherTimeframePhaseFilter.mqh",
    "backtest": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/16_higher_timeframe_f1_to_f2_confirmation_window.md",
    "phase_doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/13_higher_timeframe_f_phase_direction_filter.md",
    "obsidian": ROOT / "docs/obsidian_hook/08_entry_execution/NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window.md",
}


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"missing {label}: {token}")


def forbid(text: str, token: str, label: str, errors: list[str]) -> None:
    if token in text:
        errors.append(f"forbidden {label}: {token}")


def reference_window(f1_confirmed: bool, f2_confirmed: bool, lineage_ok: bool = True) -> bool:
    return lineage_ok and f1_confirmed and not f2_confirmed


def main() -> int:
    errors: list[str] = []
    content: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        content[name] = path.read_text(encoding="utf-8")

    if errors:
        print("NDS F2 HTF F1-to-F2 window contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    phase = content["phase"]
    backtest = content["backtest"]
    doc = content["doc"]
    phase_doc = content["phase_doc"]
    obsidian = content["obsidian"]

    require(expert, '#property version   "2.10"', "expert version", errors)
    require(expert, "InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true", "default-on input", errors)
    require(expert, "cfg.require_f1_confirmed_before_f2_confirmed_window", "config wiring", errors)
    require(types, "NDS-F2-WAIST-BREAK-12", "contract version", errors)
    require(types, "nds_f2_waist_break_point2_v12", "schema version", errors)

    require(phase, 'NDS-F2-HTF-F-PHASE-03', "phase module version", errors)
    require(phase, "FP_NDS_F2_HTF_F1_F2_WINDOW_BEFORE_F1_CONFIRM", "pre-F1 state", errors)
    require(phase, "FP_NDS_F2_HTF_F1_F2_WINDOW_OPEN", "open state", errors)
    require(phase, "FP_NDS_F2_HTF_F1_F2_WINDOW_CLOSED_AFTER_F2_CONFIRM", "post-F2 state", errors)
    require(phase, "FP_NDSF2HTFIsConfirmedF1", "F1 confirmation predicate", errors)
    require(phase, "FP_NDSF2HTFIsConfirmedF2", "F2 confirmation predicate", errors)
    require(phase, "e.parent_event_id != f1.event_id", "direct parent identity", errors)
    require(phase, "e.parent_sequence_id != f1.sequence_id", "parent sequence identity", errors)
    require(phase, "e.sequence_id == f1.sequence_id", "same sequence identity", errors)
    require(phase, "e.scale_L == f1.scale_L", "same scale identity", errors)
    require(phase, "FP_NDSF2HTFEvaluateCount", "per-count window evaluation", errors)
    forbid(phase, "lifecycle_can_spawn_f2", "spawn gate in F1 confirmation definition", errors)
    forbid(phase, "f2_can_spawn_f3", "spawn gate in F2 confirmation definition", errors)
    require(phase, "qualifying_count_total", "any-qualifying-count aggregation", errors)
    require(phase, "timebase_cfg.exclude_live_bar = true", "closed-bar semantics", errors)
    require(phase, "snapshot.source_open_bar_time == open_bar", "HTF cache", errors)
    require(backtest, "FP_NDSF2RefreshHigherTimeframePhase", "existing cached scan reuse", errors)

    require(doc, "After HTF F1 confirmation", "documented open boundary", errors)
    require(doc, "At or after the direct child HTF F2 confirmation", "documented close boundary", errors)
    require(doc, "same canonical higher-timeframe count", "same-count authority", errors)
    require(doc, "closed bars only", "documented causality", errors)
    require(phase_doc, "InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true", "phase doc input", errors)
    require(obsidian, "Exact direct-child F2 confirmed", "Obsidian close boundary", errors)

    truth_cases = [
        (False, False, True, False, "before F1"),
        (True, False, True, True, "after F1 before F2"),
        (True, True, True, False, "after F2"),
        (True, False, False, False, "lineage failure"),
    ]
    for f1, f2, lineage, expected, label in truth_cases:
        actual = reference_window(f1, f2, lineage)
        if actual != expected:
            errors.append(f"reference truth-table failure: {label}")

    runtime = "\n".join((expert, types, phase, backtest))
    forbid(runtime, "ObjectCreate(", "renderer", errors)
    forbid(runtime, "Print(", "runtime Print", errors)
    forbid(runtime, "PrintFormat(", "runtime PrintFormat", errors)

    if errors:
        print("NDS F2 HTF F1-to-F2 window contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 HTF F1-to-F2 window contract QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
