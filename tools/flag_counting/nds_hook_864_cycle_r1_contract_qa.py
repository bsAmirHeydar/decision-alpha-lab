#!/usr/bin/env python3
"""Static architecture and authority QA for the NDS Hook 86.4 Cycle R1 profile.

This verifies source contracts only. It does not replace MetaEditor compilation,
Strategy Tester replay, broker demo evidence, or operator approval.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    check_id: str
    status: str
    path: str
    detail: str


REQUIRED_FILES = (
    "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeTypes.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHook864CycleR1Rules.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeRules.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExport.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh",
    "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5",
    "mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5",
    "mql5/Experts/FlagCounting/NDSHook864CycleR1ContractSelfTest.mq5",
    "tools/flag_counting/nds_hook_864_cycle_r1_reference.py",
    "tests/flag_counting/test_nds_hook_864_cycle_r1_reference.py",
    "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/test_vectors.json",
    "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/profile_contract.json",
    "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/acceptance_matrix.json",
    "tools/flag_counting/compile_nds_hook_864_cycle_r1.ps1",
    "docs/nds_entry_architecture/phase55_hook_864_cycle_r1_execution/README.md",
    "docs/nds_hook_architecture/73_phase55_hook_864_cycle_r1_execution.md",
    "docs/obsidian_hook/03_architecture/Phase 55 NDS Hook 86.4 Cycle R1 Execution.md",
    "docs/obsidian_hook/08_entry_execution/NDS Hook 86.4 Cycle R1 Entry Contract.md",
    "docs/obsidian_hook/08_entry_execution/NDS Hook 86.4 Cycle R1 State Machine.md",
    "docs/obsidian_hook/08_entry_execution/NDS Hook 86.4 Cycle R1 Audit Ledger.md",
    "docs/obsidian_hook/08_entry_execution/NDS Hook 86.4 Cycle R1 Operator Checklist.md",
)


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="strict")


def add(checks: list[Check], ok: bool, check_id: str, path: str, detail: str) -> None:
    checks.append(Check(check_id, "PASS" if ok else "FAIL", path, detail))


def contains(checks: list[Check], root: Path, rel: str, needle: str,
             check_id: str, detail: str) -> None:
    add(checks, needle in read(root, rel), check_id, rel, detail)


def excludes(checks: list[Check], root: Path, rel: str, needle: str,
             check_id: str, detail: str) -> None:
    add(checks, needle not in read(root, rel), check_id, rel, detail)


def _strip_mql_comments_and_literals(source: str) -> str:
    """Preserve line count while removing text that must not affect delimiter QA."""
    output: list[str] = []
    index = 0
    state = "code"
    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""
        if state == "code":
            if char == "/" and next_char == "/":
                output.extend((" ", " "))
                index += 2
                state = "line_comment"
            elif char == "/" and next_char == "*":
                output.extend((" ", " "))
                index += 2
                state = "block_comment"
            elif char == '"':
                output.append(" ")
                index += 1
                state = "string"
            elif char == "'":
                output.append(" ")
                index += 1
                state = "character"
            else:
                output.append(char)
                index += 1
        elif state == "line_comment":
            output.append("\n" if char == "\n" else " ")
            if char == "\n":
                state = "code"
            index += 1
        elif state == "block_comment":
            if char == "*" and next_char == "/":
                output.extend((" ", " "))
                index += 2
                state = "code"
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        else:
            quote = '"' if state == "string" else "'"
            if char == "\\":
                output.append(" ")
                if index + 1 < len(source):
                    output.append("\n" if source[index + 1] == "\n" else " ")
                index += 2
            elif char == quote:
                output.append(" ")
                index += 1
                state = "code"
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
    return "".join(output)


def mql_delimiters_balanced(source: str) -> bool:
    cleaned = _strip_mql_comments_and_literals(source)
    stack: list[str] = []
    expected = {")": "(", "]": "[", "}": "{"}
    for char in cleaned:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != expected[char]:
                return False
    return not stack


def run(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel in REQUIRED_FILES:
        add(checks, (root / rel).is_file(), "P55_REQUIRED_FILE", rel,
            "required implementation, test, vector, or doctrine file")

    types = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeTypes.mqh"
    profile = "mql5/Include/FlagCountingPhoenix/FP_NDSHook864CycleR1Rules.mqh"
    rules = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeRules.mqh"
    core = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh"
    export = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExport.mqh"
    engine = "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh"
    backtest_engine = "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh"
    ea = "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5"
    tester = "mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5"
    diagnostic = "mql5/Experts/FlagCounting/NDSHook864CycleR1ContractSelfTest.mq5"
    reference = "tools/flag_counting/nds_hook_864_cycle_r1_reference.py"

    # Compatibility and profile isolation.
    contains(checks, root, types, "FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123 = 0",
             "P55_OLD_PROFILE_ID_STABLE", "Phase 52 profile remains enum value zero")
    contains(checks, root, types, "cfg.profile = FP_NDS_HOOK_TRADE_PROFILE_TERMINAL_F123",
             "P55_OLD_PROFILE_DEFAULT", "Phase 52 remains the reset/default behavior")
    contains(checks, root, types, "FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1 = 1",
             "P55_NEW_PROFILE_EXPLICIT", "86.4 Cycle R1 is an explicit opt-in profile")
    contains(checks, root, types, 'FP_NDS_HOOK_864_CYCLE_R1_SCHEMA_VERSION "nds_hook_864_cycle_r1_v1"',
             "P55_SCHEMA_VERSIONED", "new profile has a dedicated ledger schema")
    contains(checks, root, engine, "FP_RunNDSHookTradeExecution",
             "P55_GENERIC_ENGINE", "central engine dispatch is profile-neutral")
    contains(checks, root, engine, "FP_RunNDSHookLimitF123Execution",
             "P55_COMPATIBILITY_WRAPPER", "Phase 52 public wrapper is retained")
    contains(checks, root, core, "FP_RunNDSHookTradeExecutionCore",
             "P55_GENERIC_CORE", "shared execution core is profile-neutral")
    contains(checks, root, core, "FP_RunNDSHookLimitF123ExecutionCore",
             "P55_CORE_COMPATIBILITY_WRAPPER", "old core API is retained")

    # Exact canonical setup contract.
    contains(checks, root, types, "FP_NDS_HOOK_864_ENTRY_RATIO 0.864",
             "P55_RATIO_CONSTANT", "canonical 86.4 ratio is declared once")
    contains(checks, root, profile, "MathAbs(cfg.hook_entry_ratio - FP_NDS_HOOK_864_ENTRY_RATIO)",
             "P55_RATIO_EXACT", "profile rejects any ratio other than canonical 86.4 percent")
    contains(checks, root, profile, "cfg.hook_entry_min_x_count != FP_NDS_HOOK_864_MIN_X_COUNT",
             "P55_NODE_WINDOW_EXACT", "approved node window is exactly x3 or x4")
    contains(checks, root, profile, "confirmed_terminal_gate_must_remain_enabled",
             "P55_CONFIRMED_GATE_LOCKED", "confirmed terminal gate cannot be disabled")
    contains(checks, root, profile, "untouched_86_4_gate_must_remain_enabled",
             "P55_UNTOUCHED_GATE_LOCKED", "first-arrival gate cannot be disabled")
    contains(checks, root, types, "FP_NDS_HOOK_864_REWARD_R 1.0",
             "P55_R_CONSTANT", "canonical reward multiple is declared once")
    contains(checks, root, profile, "MathAbs(cfg.fixed_reward_r - FP_NDS_HOOK_864_REWARD_R)",
             "P55_R_EXACT", "fixed reward is exactly one R")
    contains(checks, root, profile, "FP_HookP02SequenceCycleClosed(seq)",
             "P55_CANONICAL_CYCLE_CLOSE", "cycle closure comes from canonical Hook Phase02")
    contains(checks, root, profile, "seq.resolve_confirmed",
             "P55_CANONICAL_TERMINAL", "terminal confirmation comes from canonical sequence")
    contains(checks, root, profile, "seq.x_count",
             "P55_CANONICAL_X_COUNT", "node count is consumed from canonical sequence")
    contains(checks, root, profile, "!seq.valid || seq.hook_failed || !seq.valid_hook_family",
             "P55_DIRECT_ADAPTER_VALIDITY", "direct adapter callers cannot bypass canonical validity")
    contains(checks, root, profile, "seq.valid_after_hook && cfg.allow_hook_after_hook",
             "P55_DIRECT_ADAPTER_FAMILY", "direct adapter callers cannot bypass family policy")
    contains(checks, root, profile, "canonical_price_missing",
             "P55_DIRECT_ADAPTER_PRICES", "direct adapter callers require canonical prices")
    contains(checks, root, profile, "FP_HOOK_P02_STATE_MATURE",
             "P55_MATURE_STATE", "mature canonical state is accepted")
    contains(checks, root, profile, "FP_HOOK_P02_STATE_CAPPED",
             "P55_CAPPED_STATE", "canonical x4 capped state is accepted")
    contains(checks, root, profile,
             "seq.cycle_crown_price + ratio * (seq.origin_price - seq.cycle_crown_price)",
             "P55_ENTRY_FORMULA", "entry interpolates crown toward origin at 86.4 percent")
    contains(checks, root, profile, "seq.retracement_ratio + epsilon < ratio",
             "P55_FIRST_ARRIVAL", "late orders after touching/crossing 86.4 are rejected")
    contains(checks, root, profile,
             "if(MathAbs(cfg.hook_entry_ratio - FP_NDS_HOOK_864_ENTRY_RATIO) > epsilon)",
             "P55_RATIO_GUARD_SYNTAX", "ratio guard has a complete fail-closed condition")
    contains(checks, root, profile,
             "if(MathAbs(cfg.fixed_reward_r - FP_NDS_HOOK_864_REWARD_R) > epsilon)",
             "P55_REWARD_GUARD_SYNTAX", "reward guard has a complete fail-closed condition")
    for mql_rel in (types, profile, rules, core, export, engine, backtest_engine, ea, tester, diagnostic):
        add(checks, mql_delimiters_balanced(read(root, mql_rel)),
            "P55_MQL_DELIMITER_BALANCE", mql_rel,
            "modified MQL5 source has balanced parentheses, brackets, and braces")

    # No parallel structure detector or node counter.
    for forbidden in ("CopyRates(", "CopyBuffer(", "iBarShift(", "FP_RunHookPhase02", "ArrayResize(", "for(int", "while("):
        excludes(checks, root, profile, forbidden,
                 "P55_NO_PARALLEL_HOOK_ENGINE", f"profile adapter does not own {forbidden}")
    contains(checks, root, rules, "FP_NDSHook864CycleR1SequenceEligible(seq, cfg, profile_reason)",
             "P55_EXISTING_SELECTION_PIPELINE", "existing setup selector delegates to the profile adapter")
    contains(checks, root, rules, "FP_NDSHookTradeFamilyAllowed(seq, cfg)",
             "P55_EXISTING_FAMILY_GATE", "existing HH/F3H family policy is reused")

    # Setup identity and no reprice/retry after x3 -> x4.
    contains(checks, root, rules, "Stable one-attempt identity belongs to the Hook sequence",
             "P55_STABLE_HOOK_IDENTITY", "x3/x4 terminal extension cannot create a second setup")
    contains(checks, root, rules, 'key += "|R=" + DoubleToString(cfg.hook_entry_ratio, 6)',
             "P55_PROFILE_KEY_RATIO", "profile identity includes approved ratio")
    contains(checks, root, rules, 'key += "|T=" + IntegerToString((long)seq.resolve_time)',
             "P55_PHASE52_KEY_PRESERVED", "legacy terminal profile retains terminal-time identity")
    contains(checks, root, rules, "FP_NDSHookTradeSetupUsed",
             "P55_ONE_ATTEMPT_REGISTRY", "existing persistent one-attempt registry is reused")
    contains(checks, root, rules, "GlobalVariableSetOnCondition",
             "P55_EXISTING_CAS_LOCK", "existing account-scoped compare-and-swap lock is reused")
    contains(checks, root, rules, "Preserve the exact Phase 52 broker-comment shape",
             "P55_PHASE52_COMMENT_COMPATIBILITY", "legacy Phase 52 broker comment remains unchanged")
    contains(checks, root, rules, "FP_NDSHookTradeProfileFromBrokerComment",
             "P55_PROFILE_RECOVERY_PARSER", "pending and position lifecycle recover profile ownership from broker comment")
    contains(checks, root, core, "position_profile_recovered_from_broker_comment",
             "P55_POSITION_PROFILE_RECOVERY", "restart/input changes cannot switch an existing position exit profile")
    contains(checks, root, core, "pending_profile_recovered_from_broker_comment",
             "P55_PENDING_PROFILE_RECOVERY", "restart/input changes preserve existing pending profile ownership")
    contains(checks, root, core, "FP_NDS_HOOK_864_REWARD_R",
             "P55_POSITION_CANONICAL_R", "fixed-R position verification uses immutable canonical reward")
    contains(checks, root, core, "FP_NDSHookTradeFixedRProtectionValid",
             "P55_SHARED_FIXED_R_PROTECTION", "pending and position protection share one canonical validator")
    contains(checks, root, core, "PENDING_CANCELLED_INVALID_FIXED_R_PROTECTION",
             "P55_INVALID_PENDING_CANCEL", "invalid fixed-R pending protection is cancelled fail-closed")
    contains(checks, root, core, "report.setup.reward_r =",
             "P55_RECOVERED_GEOMETRY_AUDIT", "recovered exposure writes actual broker geometry to audit fields")
    contains(checks, root, export, "report.schema_version == FP_NDS_HOOK_864_CYCLE_R1_SCHEMA_VERSION",
             "P55_RECOVERED_LEDGER_ROUTING", "restart export follows recovered profile schema rather than mutable inputs")

    # Geometry, broker normalization, risk, and order lifecycle.
    contains(checks, root, rules, "seq.death_boundary_price > 0.0 ? seq.death_boundary_price : seq.origin_price",
             "P55_STRUCTURAL_STOP_SOURCE", "stop uses canonical death boundary with origin fallback")
    contains(checks, root, rules, "SYMBOL_TRADE_STOPS_LEVEL",
             "P55_BROKER_STOP_LEVEL", "existing broker stop-level gate is reused")
    contains(checks, root, rules, "SYMBOL_TRADE_FREEZE_LEVEL",
             "P55_BROKER_FREEZE_LEVEL", "existing broker freeze-level gate is reused")
    contains(checks, root, rules, "FP_NDSHookTradeNormalizePrice",
             "P55_TICK_NORMALIZATION", "entry, stop, and target use existing tick normalization")
    contains(checks, root, rules, "setup.entry_price + setup.risk_distance * setup.reward_r",
             "P55_BULL_TARGET_1R", "bullish target is entry plus one risk distance")
    contains(checks, root, rules, "setup.entry_price - setup.risk_distance * setup.reward_r",
             "P55_BEAR_TARGET_1R", "bearish target is entry minus one risk distance")
    contains(checks, root, rules, "setup.stop_price, setup.target_price",
             "P55_ATTACHED_SL_TP", "limit request attaches both protective stop and fixed target")
    contains(checks, root, rules, "SYMBOL_ORDER_TP",
             "P55_BROKER_TP_CAPABILITY", "broker target capability is checked when target is required")
    contains(checks, root, rules, "FP_NDSHookTradeComputeVolume",
             "P55_EXISTING_SIZING", "existing fixed/risk-cash sizing is reused")
    contains(checks, root, rules, "FP_NDSHookTradeCountManagedOrders",
             "P55_EXISTING_PENDING_LOCK", "existing managed pending exposure lock is reused")
    contains(checks, root, rules, "FP_NDSHookTradeCountManagedPositions",
             "P55_EXISTING_POSITION_LOCK", "existing managed position exposure lock is reused")
    contains(checks, root, rules, "FP_NDSHookTradeCancelDeadPending",
             "P55_EXISTING_DEATH_CANCEL", "existing structural-death cancellation is reused")

    # Exit isolation and audit.
    contains(checks, root, core, "broker_sl_tp_own_exit_no_f123_close",
             "P55_NO_F123_EXIT", "fixed-R profile does not invoke F123 position close")
    contains(checks, root, core, "POSITION_HELD_BY_FIXED_R1_PROTECTION",
             "P55_POSITION_PROTECTION_VERIFIED", "open position SL/TP geometry is verified")
    contains(checks, root, core, "POSITION_WAITING_FOR_SAME_DIRECTION_F123",
             "P55_PHASE52_EXIT_PRESERVED", "legacy F123 exit remains available for old profile")
    contains(checks, root, export, "nds_hook_864_cycle_r1_trade_ledger.csv",
             "P55_DEDICATED_LEDGER", "new profile writes a dedicated audit ledger")
    contains(checks, root, export, "terminal_retracement_ratio",
             "P55_RETRACEMENT_AUDIT", "canonical terminal progress is exported")
    contains(checks, root, export, "entry_level_untouched",
             "P55_FIRST_ARRIVAL_AUDIT", "first-arrival decision is exported")
    contains(checks, root, export, "reward_r",
             "P55_R_AUDIT", "realized setup reward ratio is exported")

    # Production and tester wiring, with fail-closed live defaults.
    contains(checks, root, ea, "InpNDSHookTradeEnabled = false",
             "P55_DECISION_DEFAULT_FALSE", "central decision profile is disabled by default")
    contains(checks, root, ea, "InpNDSHookTradeSendLiveOrders = false",
             "P55_LIVE_DEFAULT_FALSE", "central broker-send authority is disabled by default")
    contains(checks, root, ea, "InpNDSHookTradeHookEntryRatio = 0.864",
             "P55_EA_RATIO_DEFAULT", "central input exposes canonical ratio")
    contains(checks, root, ea, "InpNDSHookTradeHookEntryMinXCount = 3",
             "P55_EA_X3_DEFAULT", "central input exposes canonical minimum node count")
    contains(checks, root, ea, "InpNDSHookTradeHookEntryMaxXCount = 4",
             "P55_EA_X4_DEFAULT", "central input exposes canonical maximum node count")
    contains(checks, root, ea, "FP_RunNDSHookTradeExecution",
             "P55_EA_GENERIC_WIRING", "central EA calls profile-neutral trade engine")
    contains(checks, root, tester, "InpBTTradeProfile",
             "P55_TESTER_PROFILE_INPUT", "lightweight tester can select the new profile")
    contains(checks, root, backtest_engine, "FP_RunNDSHookTradeExecutionCore",
             "P55_TESTER_SHARED_CORE", "tester and central EA share the same executable core")
    contains(checks, root, diagnostic, "NDS_HOOK_864_SELFTEST_PASS",
             "P55_MQL5_SELFTEST", "no-order MetaEditor/runtime contract diagnostic is included")
    contains(checks, root, "tools/flag_counting/compile_nds_hook_864_cycle_r1.ps1",
             "0 errors?,\\s*0 warnings?",
             "P55_METAEDITOR_COMPILE_GATE", "Windows compile script requires clean zero-error zero-warning logs")
    for forbidden in ("OrderSend(", ".BuyLimit(", ".SellLimit(", "PositionClose(", "WebRequest("):
        excludes(checks, root, diagnostic, forbidden,
                 "P55_MQL5_SELFTEST_NO_AUTHORITY", f"diagnostic excludes execution authority token {forbidden}")

    # Python mirror has no broker or process authority.
    py_text = read(root, reference)
    try:
        tree = ast.parse(py_text, filename=reference)
        add(checks, True, "P55_REFERENCE_PARSE", reference, "Python reference parses")
    except SyntaxError:
        tree = None
        add(checks, False, "P55_REFERENCE_PARSE", reference, "Python reference parses")
    forbidden_import_roots = {"socket", "subprocess", "requests", "urllib", "http", "ftplib", "smtplib"}
    forbidden_calls = {"open", "exec", "eval", "compile", "__import__"}
    authority_findings: list[str] = []
    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in forbidden_import_roots:
                        authority_findings.append(f"import:{alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if (node.module or "").split(".")[0] in forbidden_import_roots:
                    authority_findings.append(f"from:{node.module}")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in forbidden_calls:
                    authority_findings.append(f"call:{node.func.id}")
    for token in ("OrderSend", "BuyLimit", "SellLimit", "MetaTrader5", "mt5.", "WebRequest"):
        if token in py_text:
            authority_findings.append(f"token:{token}")
    add(checks, not authority_findings, "P55_REFERENCE_NO_AUTHORITY", reference,
        "reference mirror has no broker, network, subprocess, dynamic-code, or order authority")

    if not any(c.status == "FAIL" for c in checks):
        checks.append(Check(
            "P55_CONTRACT_QA", "PASS", ".",
            "all integration, canonical reuse, geometry, lifecycle, audit, compatibility, and authority checks passed",
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
