from __future__ import annotations
from tools.repository_paths import find_repository_root

import hashlib
import sys
from pathlib import Path

ROOT = find_repository_root(__file__)

FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "adapter": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2CanonicalPoint2SetupAdapter.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "trade_engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "backtest": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "contract": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/01_canonical_setup_contract.md",
    "root_fix": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/18_canonical_point2_projection_root_fix.md",
    "obsidian": ROOT / "docs/obsidian_hook/08_entry_execution/NDS F2 Canonical Point-2 Projection Root Fix.md",
}

# These are the exact hashes of the already-approved Phoenix F architecture at
# the v2.00 setup boundary. This patch is execution-only; any core mutation is a
# hard failure rather than an incidental regression.
CORE_SHA256 = {
    "mql5/Include/FlagCountingPhoenix/FP_FlagBodyEngine.mqh": "9af5e394645335d158e6d9ca830ec37f5182363abcb38aa8297e76d13da65993",
    "mql5/Include/FlagCountingPhoenix/FP_FlagBodyRules.mqh": "7d840962afe23650716ee7a3719fc4d3abf63411dbd307f19fcf40ea34a32b07",
    "mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh": "fd0f2b632dd9173bf70cf3fba5c022ceaf9fd9dfd95832f2c48231c25c84ba74",
    "mql5/Include/FlagCountingPhoenix/FP_InternalCountRules.mqh": "d01a28f5781c161ffb940bc114c33e3597e48781cbc3c15c5b06c8c852de30fb",
    "mql5/Include/FlagCountingPhoenix/FP_F1LifecycleEngine.mqh": "fabd94a0692c36ead5775889783d493435d819c17d762809fe9dc140d4cbe2bc",
    "mql5/Include/FlagCountingPhoenix/FP_F2LifecycleEngine.mqh": "d5007818ecff6605d83eb3d4b987ff38cabd288ee46c965395ff8e955e21df3c",
    "mql5/Include/FlagCountingPhoenix/FP_F2LifecycleRules.mqh": "5bbeff9f68d01230be354552926ba6404e79f521251dc1316279ee026bd5f581",
    "mql5/Include/FlagCountingPhoenix/FP_F3LifecycleEngine.mqh": "89539b1177c43e338295d3cd54559b6e7a6a99d5bfb31be37918e2af4e3b0f07",
    "mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh": "c6cce55dd5bbb8ac4fc0931e789d1a2f0698103453bd6c462eaaadb19d36a9db",
}


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"missing {label}: {token}")


def forbid(text: str, token: str, label: str, errors: list[str]) -> None:
    if token in text:
        errors.append(f"forbidden {label}: {token}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def point2_offset(requested_ticks: float, tick: float, epsilon_price: float) -> float:
    return max(max(1.0, requested_ticks) * tick, max(0.0, epsilon_price) + tick)


def main() -> int:
    errors: list[str] = []
    content: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        content[name] = path.read_text(encoding="utf-8")

    for rel, expected in CORE_SHA256.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing protected core file: {rel}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"protected core mutated: {rel}: {actual} != {expected}")

    if errors:
        print("NDS F2 canonical Point-2 projection root-fix QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    adapter = content["adapter"]
    setup = content["setup"]
    types = content["types"]
    rules = content["rules"]
    trade_engine = content["trade_engine"]
    backtest = content["backtest"]
    contract = content["contract"]
    root_fix = content["root_fix"]
    obsidian = content["obsidian"]

    require(expert, '#property version   "2.10"', "expert version", errors)
    require(types, "NDS-F2-WAIST-BREAK-12", "contract version", errors)
    require(types, "nds_f2_waist_break_point2_v12", "schema version", errors)

    require(adapter, "This module does not detect, rebuild, reinterpret, or mutate F1/F2/F3", "authority boundary", errors)
    require(adapter, "F2 flag body       = Origin -> Leg1 -> Waist -> Leg2", "body semantics", errors)
    require(adapter, "F2 post-flag phase = internal count / Waist-break branch", "post-flag semantics", errors)
    require(adapter, "F2 confirmation   = favorable re-break of the original F2 flag end", "confirmation semantics", errors)
    require(adapter, "projected Point 1 = the already-existing F2 flag Waist", "Point-1 projection", errors)
    require(adapter, "executable Point 2 = the first strict price passage beyond that Waist", "Point-2 projection", errors)
    require(adapter, "f2.f2_body_complete", "body-ready gate", errors)
    require(adapter, "f2.status == FP_STATUS_CONFIRMED", "confirmed-source rejection", errors)
    require(adapter, "f2.f2_lifecycle_status == FP_F2_LC_INVALIDATED", "invalid-source rejection", errors)
    require(adapter, "f2.status != FP_STATUS_POST_FLAG", "post-flag eligibility awareness", errors)
    require(adapter, "FP_EpsilonPrice(epsilon_points)) + tick", "epsilon plus tick boundary", errors)
    require(adapter, "FP_NDSF2SameCanonicalBodyIdentity", "source-body identity matcher", errors)

    require(setup, '#include "FP_NDSF2CanonicalPoint2SetupAdapter.mqh"', "adapter inclusion", errors)
    require(setup, "setup.f2_body_id = f2.body_id", "body identity capture", errors)
    require(setup, "setup.projected_waist_break_branch = true", "projected branch marker", errors)
    require(setup, "FP_NDSF2CanonicalPoint2OffsetPrice", "strict Point-2 pricing", errors)
    require(setup, "setup.target_price = FP_NDSF2NormalizeNearest(symbol, f2.leg2.price)", "original flag-end target", errors)
    require(setup, "FP_NDSF2LevelTouchedSinceAvailability", "causal missed-level rejection", errors)

    require(types, "f2_body_id", "setup body identity field", errors)
    require(types, "canonical_break_epsilon_price", "epsilon audit field", errors)
    require(types, "canonical_point2_min_offset_price", "Point-2 offset audit field", errors)
    require(types, "FP_NDS_F2_RUN_PENDING_CANCELLED_SOURCE_LIFECYCLE", "source cancellation result", errors)

    require(rules, "struct FP_NDSF2ActiveAttempt", "active attempt source binding", errors)
    require(rules, "f2_flag_end_price", "dynamic TP=0 target fallback", errors)
    require(rules, "FP_NDSF2ActiveAttemptSourceStillAlive", "source lifecycle resolver", errors)
    require(rules, "FP_NDSF2CancelPendingOrdersWithDeadSource", "source lifecycle cancellation", errors)
    require(rules, "target = g_fp_nds_f2_active_attempts[attempt_index].f2_flag_end_price", "dynamic target recovery", errors)
    require(rules, "FP_NDSF2RegisterActiveAttempt(ticket, setup)", "full source registration", errors)

    require(trade_engine, "FP_NDSF2CancelPendingOrdersWithDeadSource", "per-cycle source reconciliation", errors)
    require(trade_engine, "pending_cancelled_source_lifecycle", "source cancellation funnel", errors)
    require(backtest, "needs_pending_source_lifecycle_detection", "closed-bar pending source scan", errors)
    require(backtest, "pending_source_lifecycle_scan", "hold-path bypass", errors)

    require(contract, "F2 flag body:", "documented flag body", errors)
    require(contract, "Then F2 post-flag correction:", "documented post-flag phase", errors)
    require(contract, "Then F2 confirmation:", "documented confirmation", errors)
    require(contract, "The fill is the executable Point 2", "documented entry event", errors)
    require(root_fix, "The execution profile is corrected as a consumer adapter", "root-fix boundary", errors)
    require(root_fix, "Files deliberately not modified", "protected-core declaration", errors)
    require(obsidian, "The execution layer does not redefine any of these stages", "Obsidian authority boundary", errors)

    runtime = "\n".join((expert, adapter, setup, types, rules, trade_engine, backtest))
    forbid(runtime, "ObjectCreate(", "rendering path", errors)
    forbid(runtime, "ChartRedraw(", "chart redraw", errors)
    forbid(adapter, "Print(", "adapter runtime print", errors)
    forbid(adapter, "PrintFormat(", "adapter runtime print format", errors)
    forbid(adapter, "FileOpen(", "adapter file I/O", errors)
    forbid(adapter, "OnTimer", "adapter timer", errors)

    # Reference geometry checks independent of MQL runtime.
    if abs(point2_offset(1.0, 0.25, 1.0) - 1.25) > 1e-12:
        errors.append("reference offset failed: epsilon must dominate one requested tick")
    if abs(point2_offset(8.0, 0.25, 1.0) - 2.0) > 1e-12:
        errors.append("reference offset failed: user request must dominate epsilon")
    if abs(point2_offset(0.0, 0.25, 0.0) - 0.25) > 1e-12:
        errors.append("reference offset failed: minimum one tick")

    if errors:
        print("NDS F2 canonical Point-2 projection root-fix QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 canonical Point-2 projection root-fix QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
