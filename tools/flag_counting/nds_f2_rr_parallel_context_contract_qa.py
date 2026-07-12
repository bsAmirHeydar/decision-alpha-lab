from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "trade_engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "backtest_engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/10_reward_risk_and_parallel_context_policy.md",
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
        print("NDS F2 RR / parallel-context contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    setup = content["setup"]
    rules = content["rules"]
    trade_engine = content["trade_engine"]
    backtest_engine = content["backtest_engine"]
    doc = content["doc"]

    require(expert, '#property version   "1.50"', "expert version", errors)
    require(expert, "InpF2BTUseMinimumRewardRiskFilter = true", "RR filter default", errors)
    require(expert, "InpF2BTAdjustEntryToMinimumRewardRisk = true", "RR repricing default", errors)
    require(expert, "InpF2BTMinimumRewardRisk = 1.0", "minimum RR default", errors)
    require(expert, "InpF2BTUseStopSpaceOverlapDeduplication = true", "overlap dedup default", errors)
    require(expert, "InpF2BTStopSpaceOverlapThresholdPercent = 80.0", "overlap threshold default", errors)
    require(expert, "InpF2BTAllowOppositeDirectionHedge = true", "hedge default", errors)
    require(expert, "InpF2BTAllowSameDirectionMultipleContexts = true", "same-direction default", errors)
    require(expert, "InpF2BTMaxConcurrentManagedExposures = 0", "unlimited cap default", errors)

    require(types, "use_min_reward_risk_filter", "RR config field", errors)
    require(types, "adjust_entry_to_min_reward_risk", "RR repricing field", errors)
    require(types, "min_reward_risk", "RR threshold field", errors)
    require(types, "use_stop_space_overlap_deduplication", "overlap dedup field", errors)
    require(types, "stop_space_overlap_percent", "overlap threshold field", errors)
    require(types, "allow_opposite_direction_hedge", "hedge config field", errors)
    require(types, "allow_same_direction_multiple_contexts", "same-direction config field", errors)
    require(types, "reward_risk", "setup RR evidence", errors)

    require(setup, "setup.risk_distance = MathAbs(setup.entry_price - setup.stop_price)", "risk distance", errors)
    require(setup, "setup.reward_distance = MathAbs(setup.target_price - setup.entry_price)", "reward distance", errors)
    require(setup, "setup.reward_risk = setup.reward_distance / setup.risk_distance", "RR formula", errors)
    require(setup, "Entry = (Target + required_rr * Stop) / (1 + required_rr)", "RR repricing equation comment", errors)
    require(setup, "FP_NDSF2AdjustEntryForMinimumRewardRisk", "RR repricing helper", errors)
    require(setup, "setup.entry_adjusted_for_reward_risk", "RR adjustment evidence", errors)
    require(setup, "FP_NDSF2CollectWaistBreakPairs", "all-context collector", errors)

    require(rules, "FP_NDSF2ExposurePolicyAllows", "exposure policy", errors)
    require(rules, "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING", "hedging account boundary", errors)
    require(rules, "same_direction_context_disabled", "same-direction blocker", errors)
    require(rules, "opposite_direction_hedge_disabled", "hedge blocker", errors)
    require(rules, "parallel_context_requires_hedging_account", "netting blocker", errors)
    require(rules, "FP_NDSF2CancelConsumedPendingOrders", "per-order target reconciliation", errors)
    require(rules, "FP_NDSF2StopSpaceOverlapPercent", "stop-corridor overlap", errors)
    require(rules, "overlapping_pending_is_equal_or_wider", "wider pending arbitration", errors)

    require(trade_engine, "FP_NDSF2SameDirectionNearDuplicate", "same-bar overlap arbitration", errors)
    require(trade_engine, "FP_NDSF2SetupIsWider", "wider candidate selection", errors)
    require(trade_engine, "FP_NDS_F2_RUN_MULTI_ORDER_SENT", "multi-send result", errors)
    require(backtest_engine, "hard_parallel_block", "fast blocked-exposure path", errors)
    require(backtest_engine, "FP_NDSF2AccountSupportsIndependentContexts", "account-aware fast path", errors)

    require(doc, "Reward/Risk     = Reward Distance / Risk Distance", "documented RR", errors)
    require(doc, "InpF2BTAllowSameDirectionMultipleContexts = true", "documented same-direction default", errors)
    require(doc, "InpF2BTAllowOppositeDirectionHedge = true", "documented hedge default", errors)
    require(doc, "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING", "documented account boundary", errors)

    runtime = "\n".join(content[name] for name in (
        "expert", "types", "setup", "rules", "trade_engine", "backtest_engine"
    ))
    forbid(runtime, "Print(", "custom runtime Print", errors)
    forbid(runtime, "PrintFormat(", "custom runtime PrintFormat", errors)
    forbid(runtime, "FileOpen(", "runtime file I/O", errors)
    forbid(runtime, "ObjectCreate(", "runtime chart objects", errors)

    if errors:
        print("NDS F2 RR / parallel-context contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 RR / parallel-context contract QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
