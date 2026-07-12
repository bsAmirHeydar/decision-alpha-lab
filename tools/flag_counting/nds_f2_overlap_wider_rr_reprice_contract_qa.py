from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "backtest": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/11_overlap_arbitration_and_rr_entry_repricing.md",
    "obsidian": ROOT / "docs/obsidian_hook/08_entry_execution/NDS F2 Overlap Wider and RR Repricing.md",
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
        print("NDS F2 overlap-wider / RR-reprice contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    setup = content["setup"]
    rules = content["rules"]
    engine = content["engine"]
    backtest = content["backtest"]
    doc = content["doc"]
    obsidian = content["obsidian"]

    require(expert, '#property version   "1.50"', "expert version", errors)
    require(expert, "InpF2BTAdjustEntryToMinimumRewardRisk = true", "RR adjustment default", errors)
    require(expert, "InpF2BTUseStopSpaceOverlapDeduplication = true", "overlap dedup default", errors)
    require(expert, "InpF2BTStopSpaceOverlapThresholdPercent = 80.0", "overlap default", errors)

    require(types, 'NDS-F2-WAIST-BREAK-06', "contract version", errors)
    require(types, "adjust_entry_to_min_reward_risk", "RR adjustment config", errors)
    require(types, "use_stop_space_overlap_deduplication", "overlap config", errors)
    require(types, "stop_space_overlap_percent", "overlap threshold config", errors)
    require(types, "structural_entry_price", "structural entry evidence", errors)
    require(types, "entry_adjusted_for_reward_risk", "adjusted entry evidence", errors)

    require(setup, "Entry = (Target + required_rr * Stop) / (1 + required_rr)", "RR equation", errors)
    require(setup, "FP_NDSF2AdjustEntryForMinimumRewardRisk", "RR adjustment function", errors)
    require(setup, "FP_NDSHookTradeNormalizePrice(symbol, raw_entry, false)", "bullish round toward stop", errors)
    require(setup, "FP_NDSHookTradeNormalizePrice(symbol, raw_entry, true)", "bearish round toward stop", errors)
    require(setup, "setup.reward_risk + 1e-12 <", "final RR verification", errors)

    require(rules, "FP_NDSF2StopSpaceOverlapPercent", "overlap equation", errors)
    require(rules, "100.0 * intersection / narrower", "narrower denominator", errors)
    require(rules, "FP_NDSF2SameDirectionNearDuplicate", "same-direction dedup", errors)
    require(rules, "overlapping_pending_is_equal_or_wider", "wider pending winner", errors)
    require(rules, "overlapping_position_already_filled", "filled-position ownership", errors)
    require(rules, "FP_NDSF2DeletePendingOrder", "narrower pending replacement", errors)

    require(engine, "Build all executable candidates before any order is sent", "same-bar pre-arbitration", errors)
    require(engine, "FP_NDSF2SetupIsWider", "wider candidate selection", errors)
    require(engine, "suppressed[j] = true", "narrower suppression", errors)

    require(backtest, "pending_replacement_scan", "replacement scan fast-path exception", errors)

    require(doc, "Overlap % = length(intersection(A, B)) / min(width(A), width(B)) × 100", "documented overlap", errors)
    require(doc, "Entry* = (Target + Rmin × Stop) / (1 + Rmin)", "documented repricing", errors)
    require(obsidian, "The wider corridor wins", "Obsidian wider rule", errors)


    # Numeric contract examples independent of source-token checks.
    def overlap_percent(entry_a: float, stop_a: float, entry_b: float, stop_b: float) -> float:
        lo_a, hi_a = sorted((entry_a, stop_a))
        lo_b, hi_b = sorted((entry_b, stop_b))
        intersection = max(0.0, min(hi_a, hi_b) - max(lo_a, lo_b))
        narrower = min(hi_a - lo_a, hi_b - lo_b)
        return 0.0 if narrower <= 0.0 else 100.0 * intersection / narrower

    if abs(overlap_percent(100.0, 90.0, 102.0, 92.0) - 80.0) > 1e-9:
        errors.append("numeric overlap example did not equal 80%")

    def required_entry(target: float, stop: float, rr: float) -> float:
        return (target + rr * stop) / (1.0 + rr)

    if abs(required_entry(110.0, 90.0, 1.0) - 100.0) > 1e-9:
        errors.append("bullish RR=1 repricing example failed")
    if abs(required_entry(90.0, 110.0, 1.0) - 100.0) > 1e-9:
        errors.append("bearish RR=1 repricing example failed")

    runtime = "\n".join(content[name] for name in (
        "expert", "types", "setup", "rules", "engine", "backtest"
    ))
    forbid(runtime, "Print(", "runtime print", errors)
    forbid(runtime, "PrintFormat(", "runtime printformat", errors)
    forbid(runtime, "FileOpen(", "runtime file IO", errors)
    forbid(runtime, "ObjectCreate(", "runtime chart object", errors)

    if errors:
        print("NDS F2 overlap-wider / RR-reprice contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 overlap-wider / RR-reprice contract QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
