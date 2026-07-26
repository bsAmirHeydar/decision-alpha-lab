#!/usr/bin/env python3
"""Static contract QA for NDS Phase 52 Hook limit/F123 execution.

This is a source-contract preflight. It is not a substitute for MetaEditor
compilation, broker demo testing, or visual chart validation.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    check_id: str
    status: str
    path: str
    detail: str


REQUIRED_FILES = (
    "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeTypes.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeRules.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExport.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh",
    "docs/contexts/legacy/nds/entry/phase52_hook_limit_f123_execution/README.md",
    "docs/contexts/legacy/nds/entry/phase52_hook_limit_f123_execution/03_single_exposure_state_machine.md",
    "docs/contexts/legacy/nds/entry/phase52_hook_limit_f123_execution/04_same_direction_f123_exit.md",
    "docs/history/obsidian/hook/00_mocs/NDS_ENTRY_EXECUTION_MOC.md",
    "docs/history/obsidian/hook/03_architecture/Phase 52 NDS Hook Limit F123 Execution.md",
    "docs/history/obsidian/hook/08_entry_execution/NDS Hook Limit Entry Contract.md",
    "docs/history/obsidian/hook/08_entry_execution/NDS Single Exposure Lock.md",
    "docs/history/obsidian/hook/08_entry_execution/NDS Same Direction F123 Exit.md",
)


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="ignore")


def contains(checks: list[Check], root: Path, rel: str, needle: str,
             check_id: str, detail: str) -> None:
    ok = needle in read(root, rel)
    checks.append(Check(check_id, "PASS" if ok else "FAIL", rel, detail))


def excludes(checks: list[Check], root: Path, rel: str, needle: str,
             check_id: str, detail: str) -> None:
    ok = needle not in read(root, rel)
    checks.append(Check(check_id, "PASS" if ok else "FAIL", rel, detail))


def run(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_FILES:
        checks.append(Check(
            "P52_REQUIRED_FILE",
            "PASS" if (root / rel).is_file() else "FAIL",
            rel,
            "required Phase 52 implementation or authority file",
        ))

    ea = "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5"
    types = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeTypes.mqh"
    rules = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeRules.mqh"
    export = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExport.mqh"
    core = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh"
    engine = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh"

    contains(checks, root, ea, '#property version   "18.41"',
             "P52_EA_VERSION", "central EA is versioned for Phase 52.1")
    contains(checks, root, ea, "InpNDSHookTradeEnabled = false",
             "P52_ENABLE_DEFAULT_FALSE", "strategy decision engine is disabled by default")
    contains(checks, root, ea, "InpNDSHookTradeSendLiveOrders = false",
             "P52_SEND_DEFAULT_FALSE", "broker-send authority is disabled by default")
    contains(checks, root, ea, "FP_RunNDSHookTradeExecution",
             "P52_ENGINE_WIRED", "central EA uses the profile-neutral Hook trade engine")
    contains(checks, root, engine, "FP_RunNDSHookTradeExecutionCore",
             "P52_SHARED_CORE_WRAPPER", "production engine delegates to the shared execution core")
    contains(checks, root, engine, "FP_RunNDSHookLimitF123Execution",
             "P52_COMPATIBILITY_WRAPPER", "legacy Phase 52 public API remains available")

    contains(checks, root, rules, "seq.valid_after_hook",
             "P52_SOURCE_HH", "Hook-after-Hook source is explicit")
    contains(checks, root, rules, "seq.valid_after_opposing_f3",
             "P52_SOURCE_F3H", "Hook-after-opposing-F3 source is explicit")
    contains(checks, root, rules, "!seq.valid || seq.hook_failed || !seq.valid_hook_family",
             "P52_VALID_HOOK_GATE", "invalid or failed Hook is rejected")
    contains(checks, root, rules, "seq.resolve_price",
             "P52_TERMINAL_ENTRY", "entry uses canonical raw Hook terminal")
    contains(checks, root, rules, "BuyLimit(setup.volume, setup.entry_price",
             "P52_BUY_LIMIT", "positive/bullish Hook submits Buy Limit")
    contains(checks, root, rules, "SellLimit(setup.volume, setup.entry_price",
             "P52_SELL_LIMIT", "negative/bearish Hook submits Sell Limit")
    contains(checks, root, types, "s.target_price = 0.0",
             "P52_NO_FIXED_TP_DEFAULT", "legacy profile reset has no fixed target")
    contains(checks, root, rules, "double raw_entry = seq.resolve_price",
             "P52_TERMINAL_RAW_ENTRY_PRESERVED", "legacy profile still starts from canonical terminal")
    contains(checks, root, rules, "setup.stop_price, setup.target_price",
             "P52_SHARED_SEND_GEOMETRY", "shared sender consumes profile-owned target; legacy target remains zero")
    contains(checks, root, rules, "death_boundary_price",
             "P52_DEATH_STOP", "protective stop derives from Hook death/origin")

    contains(checks, root, rules, "FP_NDSHookTradeCountManagedOrders",
             "P52_PENDING_COUNT", "pending exposure is counted by strategy magic")
    contains(checks, root, rules, "FP_NDSHookTradeCountManagedPositions",
             "P52_POSITION_COUNT", "position exposure is counted by strategy magic")
    contains(checks, root, rules, "GlobalVariableSetOnCondition",
             "P52_COMPARE_SWAP_LOCK", "terminal-wide compare-and-swap lock prevents entry race")
    contains(checks, root, core, "BLOCKED_EXPOSURE_CHANGED_DURING_ENTRY",
             "P52_SECOND_EXPOSURE_CHECK", "broker state is rechecked while entry lock is held")
    contains(checks, root, rules, "FP_NDSHookTradeReconcileDuplicatePending",
             "P52_DUPLICATE_PENDING_RECOVERY", "duplicate pending orders are reconciled")
    contains(checks, root, core, "INVARIANT_MULTIPLE_MANAGED_POSITIONS",
             "P52_MULTIPLE_POSITION_FAIL_CLOSED", "multiple live positions require manual reconciliation")

    contains(checks, root, rules, "FP_NDSHookTradeFindF123Evidence",
             "P52_EXPLICIT_F123", "exit requires explicit F1 and F2 chain evidence")
    contains(checks, root, rules, "events[i].level == FP_LEVEL_F1",
             "P52_F1_REQUIRED", "F1 evidence is required")
    contains(checks, root, rules, "events[i].level == FP_LEVEL_F2",
             "P52_F2_REQUIRED", "F2 evidence is required")
    contains(checks, root, rules, "e.level != FP_LEVEL_F3",
             "P52_F3_REQUIRED", "F3 evidence is required")
    contains(checks, root, rules, "e.direction != position_direction",
             "P52_SAME_DIRECTION_EXIT", "exit F3 must match position direction")
    contains(checks, root, rules, "f1_start <= position_open_time || f2_start <= position_open_time",
             "P52_FULL_CHAIN_AFTER_ENTRY", "strict gate requires F1/F2 after broker fill")
    contains(checks, root, rules, "PositionClose(position_ticket",
             "P52_CLOSE_BY_TICKET", "exit closes the managed position by ticket")
    contains(checks, root, rules, "close_request_accepted_but_position_still_open",
             "P52_CLOSE_VERIFICATION", "accepted close is verified against open position state")

    contains(checks, root, rules, "FP_NDSHookTradeSetupUsed",
             "P52_ONE_ATTEMPT_REGISTRY", "one-attempt-per-Hook persistence exists")
    contains(checks, root, rules, "AccountInfoInteger(ACCOUNT_LOGIN)",
             "P52_ACCOUNT_SCOPED_STATE", "persistent keys and locks are account scoped")
    contains(checks, root, export, "nds_hook_limit_f123_trade_ledger.csv",
             "P52_AUDIT_LEDGER", "Phase 52 exports a dedicated lifecycle ledger")
    contains(checks, root, export, "exit_f2_start",
             "P52_F2_AUDIT", "F2 start is preserved in the exit evidence ledger")

    # Economic ownership remains magic-based. Broker comments are consulted only
    # after magic/symbol ownership is established, to recover the immutable
    # lifecycle profile across terminal restart or input-profile changes.
    contains(checks, root, core, "PositionGetInteger(POSITION_MAGIC) != cfg.magic",
             "P52_MAGIC_POSITION_AUTHORITY", "position economic ownership remains strategy-magic based")
    contains(checks, root, rules, "OrderGetInteger(ORDER_MAGIC) != cfg.magic",
             "P52_MAGIC_ORDER_AUTHORITY", "order economic ownership remains strategy-magic based")
    contains(checks, root, core, "FP_NDSHookTradeProfileFromBrokerComment",
             "P52_PROFILE_RECOVERY_AFTER_OWNERSHIP", "managed exposure lifecycle profile is recovered after magic ownership")
    contains(checks, root, core, "BLOCKED_MANAGED_POSITION_PROFILE_UNKNOWN",
             "P52_UNKNOWN_POSITION_PROFILE_FAIL_CLOSED", "unknown managed-position profile fails closed")
    contains(checks, root, core, "BLOCKED_MANAGED_PENDING_PROFILE_UNKNOWN",
             "P52_UNKNOWN_PENDING_PROFILE_FAIL_CLOSED", "unknown managed-pending profile fails closed")
    excludes(checks, root, rules, "ORDER_COMMENT) !=",
             "P52_NO_COMMENT_EQUALITY_OWNERSHIP", "order ownership does not use mutable comment equality")

    if not any(c.status == "FAIL" for c in checks):
        checks.append(Check(
            "P52_CONTRACT_QA", "PASS", ".",
            "all Phase 52 source, entry, single-exposure, exit, and audit contracts passed",
        ))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    checks = run(root)
    for item in checks:
        print(f"{item.status}\t{item.check_id}\t{item.path}\t{item.detail}")
    return 1 if any(c.status == "FAIL" for c in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
