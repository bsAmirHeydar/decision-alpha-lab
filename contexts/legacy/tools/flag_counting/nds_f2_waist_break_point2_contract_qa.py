from __future__ import annotations
from tools.repository_paths import find_repository_root

import sys
from pathlib import Path

ROOT = find_repository_root(__file__)

FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "detector": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "adapter": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2CanonicalPoint2SetupAdapter.mqh",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "bt": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/01_canonical_setup_contract.md",
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
        print("\n".join(errors))
        return 1

    expert = content["expert"]
    detector = content["detector"]
    setup = content["setup"]
    adapter = content["adapter"]
    rules = content["rules"]
    engine = content["engine"]
    bt = content["bt"]
    doc = content["doc"]

    require(expert, '#property version   "2.10"', "expert version", errors)
    require(expert, "InpF2BTEntryBehindF2WaistTicks", "entry offset input", errors)
    require(expert, "InpF2BTStopBehindF1WaistTicks", "stop offset input", errors)
    require(expert, "InpF2BTMinimumRewardRisk = 1.0", "default minimum RR", errors)
    require(expert, "InpF2BTAllowOppositeDirectionHedge = true", "default hedge policy", errors)
    require(expert, "InpF2BTAllowSameDirectionMultipleContexts = true", "default same-direction policy", errors)
    require(expert, "cfg.f2_show_post_flag_candidates = true", "unconfirmed F2 visibility", errors)
    require(expert, "cfg.f2_show_live_body_candidates = true", "F2 body candidate visibility", errors)
    require(expert, "cfg.scan_hooks = false", "Hook disable", errors)
    require(expert, "cfg.scan_f3 = FP_NDSF2ExitModeUsesEntryTimeframeF3(InpF2BTExitMode)", "mode-aware F3 scan", errors)

    require(adapter, "projected Point 1 = the already-existing F2 flag Waist", "Point-1 projection contract", errors)
    require(adapter, "It is not evidence that the whole F2 has confirmed", "confirmation exclusion", errors)
    require(adapter, "f2.f2_body_complete", "body-complete trigger", errors)
    require(adapter, "f2.status == FP_STATUS_CONFIRMED", "confirmed-F2 rejection", errors)
    require(setup, "f2.waist.price - entry_offset", "bullish entry behind waist", errors)
    require(setup, "f2.waist.price + entry_offset", "bearish entry behind waist", errors)
    require(setup, "f1.waist.price - stop_offset", "bullish stop behind F1 waist", errors)
    require(setup, "f1.waist.price + stop_offset", "bearish stop behind F1 waist", errors)
    require(setup, "setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price)", "Leg2 target", errors)
    require(adapter, "FP_EpsilonPrice(epsilon_points)) + tick", "epsilon-aware strict entry penetration", errors)
    require(setup, "MathMax(1.0, cfg.stop_behind_f1_waist_ticks)", "strict stop penetration", errors)
    require(setup, "events[i].leg2", "Leg2 observability", errors)
    require(setup, "setup.reward_risk = setup.reward_distance / setup.risk_distance", "RR calculation", errors)
    require(setup, "FP_NDSF2AdjustEntryForMinimumRewardRisk", "minimum RR entry adjustment", errors)
    require(setup, "FP_NDSF2CollectWaistBreakPairs", "multi-context collection", errors)

    require(detector, "FP_BuildCanonicalNodesForScale", "canonical node reuse", errors)
    require(detector, "FP_TryBuildFlagChainsFromOrigins", "canonical F1/F2 lifecycle reuse", errors)
    forbid(detector, "FP_BuildHookBranches", "Hook construction", errors)
    forbid(detector, "FP_DetectScale(", "general heavy detector", errors)

    require(rules, "TRADE_ACTION_PENDING", "pending request", errors)
    require(rules, "ORDER_TYPE_BUY_LIMIT", "buy limit", errors)
    require(rules, "ORDER_TYPE_SELL_LIMIT", "sell limit", errors)
    require(rules, "FP_NDSF2PendingTargetConsumed", "target-consumption check", errors)
    require(rules, "TRADE_ACTION_REMOVE", "stale pending removal", errors)
    require(rules, "OrderCheck", "broker precheck", errors)
    require(rules, "OrderSend", "tester order send", errors)
    require(rules, "FP_NDSF2ExposurePolicyAllows", "parallel exposure policy", errors)
    require(rules, "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING", "hedging account guard", errors)
    require(rules, "allow_same_direction_multiple_contexts", "same-direction context switch", errors)
    require(rules, "allow_opposite_direction_hedge", "opposite hedge switch", errors)

    require(engine, "FP_NDSF2CollectWaistBreakPairs", "waist-break context collector", errors)
    require(engine, "FP_NDSF2BuildWaistBreakSetup", "waist-break setup builder", errors)
    require(bt, "FP_NDS_F2_RUN_PENDING_CANCELLED_TARGET_CONSUMED", "pending cancellation state", errors)
    require(bt, "FP_NDSF2CancelConsumedPendingOrders", "multi-pending reconciliation", errors)

    require(doc, "Point 1 = the Waist of the already-complete two-leg F2 flag body", "documented Point 1", errors)
    require(doc, "For the fixed exit mode:", "documented fixed exit", errors)
    require(doc, "F2 confirmation remains a later Phoenix lifecycle event", "documented timing", errors)

    # Runtime cleanliness. The only optional I/O is one deinit-only funnel row
    # inside the rules module, disabled by default.
    require(expert, "InpF2BTEnableFunnelDiagnostics = false", "diagnostics default-off", errors)
    require(rules, "if(!cfg.enable_funnel_diagnostics) return;", "diagnostics opt-in guard", errors)
    for name in ("expert", "detector", "setup", "adapter", "engine", "bt"):
        text = content[name]
        forbid(text, "Print(", f"custom Print in {name}", errors)
        forbid(text, "PrintFormat(", f"custom PrintFormat in {name}", errors)
        forbid(text, "FileOpen(", f"unexpected file I/O in {name}", errors)
        forbid(text, "ObjectCreate(", f"chart object path in {name}", errors)
    forbid(rules, "Print(", "custom Print in rules", errors)
    forbid(rules, "PrintFormat(", "custom PrintFormat in rules", errors)
    forbid(rules, "ObjectCreate(", "chart object path in rules", errors)

    if errors:
        print("NDS F2 waist-break Point-2 contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 waist-break Point-2 contract QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
