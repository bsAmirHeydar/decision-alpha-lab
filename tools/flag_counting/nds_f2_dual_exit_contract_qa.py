from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "rules": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh",
    "manager": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2F3ExitManager.mqh",
    "engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh",
    "backtest": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/12_dual_exit_fixed_f2_and_f3_flag_retest.md",
    "obsidian": ROOT / "docs/obsidian_hook/08_entry_execution/NDS F2 Dual Exit - Fixed F2 or F3 Retest.md",
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
        print("NDS F2 dual-exit contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    setup = content["setup"]
    rules = content["rules"]
    manager = content["manager"]
    engine = content["engine"]
    backtest = content["backtest"]
    doc = content["doc"]
    obsidian = content["obsidian"]

    require(expert, '#property version   "1.80"', "expert version", errors)
    require(expert, "InpF2BTExitMode = FP_NDS_F2_EXIT_FIXED_F2_FLAG_END", "default fixed exit", errors)
    require(expert, "InpF2BTF3ExitCorrectionTicks = 1.0", "default correction gate", errors)
    require(expert, "InpF2BTCloseAtMarketIfF3TargetAlreadyReached = true", "market fallback default", errors)
    require(expert, "FP_NDSF2ManageDynamicExitOnTick", "per-tick dynamic manager", errors)
    require(expert, "cfg.scan_f3 = FP_NDSF2ExitModeUsesEntryTimeframeF3(InpF2BTExitMode)", "dynamic exact F3 scan", errors)

    require(types, "FP_NDS_F2_EXIT_FIXED_F2_FLAG_END", "fixed exit enum", errors)
    require(types, "FP_NDS_F2_EXIT_F3_FLAG_RETEST", "dynamic exit enum", errors)
    require(types, "rr_reference_target_price", "RR reference field", errors)
    require(types, "initial_broker_take_profit_price", "initial broker TP field", errors)
    require(types, "FP_NDSF2DynamicExitContext", "dynamic context type", errors)
    require(types, "NDS-F2-WAIST-BREAK-09", "contract version", errors)

    require(setup, "setup.rr_reference_target_price = setup.target_price", "F2 Leg2 RR authority", errors)
    require(setup, "FP_NDS_F2_EXIT_FIXED_F2_FLAG_END ? setup.target_price : 0.0", "mode-aware initial TP", errors)
    require(setup, "FP_NDSF2ExitModeUsesEntryTimeframeF3(cfg.exit_mode)", "dynamic F2 size authority", errors)
    require(setup, "FP_NDSF2AdjustEntryForMinimumRewardRisk", "unchanged RR repricing", errors)

    require(rules, "request.tp = setup.initial_broker_take_profit_price", "mode-aware pending TP", errors)
    require(rules, "FP_NDSF2RegisterDynamicExitContext", "dynamic context registration", errors)
    require(rules, "FP_NDSF2DeactivateDynamicContextByOrderTicket", "context cleanup on order delete", errors)

    require(manager, "child_f3.leg1.price", "exact child F3 target capture", errors)
    require(manager, "f2.f2_can_spawn_f3", "canonical F3 authorization", errors)
    require(manager, "child_f3.has_waist", "canonical F3 waist correction gate", errors)
    require(manager, "TRADE_ACTION_SLTP", "dynamic TP modification", errors)
    require(manager, "PositionClose", "already-reached market close fallback", errors)
    require(manager, "ORDER_POSITION_ID", "order-position binding", errors)
    require(manager, "POSITION_IDENTIFIER", "position identity binding", errors)
    require(manager, "reference_target_price", "dynamic pending consumption reference", errors)

    require(engine, "FP_NDSF2UpdateDynamicExitFromEvents", "new-bar confirmation update", errors)
    require(backtest, "FP_NDSF2ManageDynamicExitOnTick", "immediate post-detection arm", errors)

    require(doc, "Mode A — FIXED_F2_FLAG_END", "fixed mode documentation", errors)
    require(doc, "Mode B — F3_FLAG_RETEST", "dynamic mode documentation", errors)
    require(doc, "RR Reference Target = original F2 Leg2", "RR reference documentation", errors)
    require(doc, "F3 Leg1 = F2 confirmation node", "canonical equivalence documentation", errors)
    require(obsidian, "original F2 Leg2 = RR reference only", "Obsidian dynamic summary", errors)

    runtime = "\n".join(content[name] for name in (
        "expert", "types", "setup", "rules", "manager", "engine", "backtest"
    ))
    forbid(runtime, "Print(", "runtime Print", errors)
    forbid(runtime, "PrintFormat(", "runtime PrintFormat", errors)
    forbid(runtime, "FileOpen(", "runtime file IO", errors)
    forbid(runtime, "ObjectCreate(", "runtime renderer", errors)
    require(runtime, "FP_NDSF2ExactChildF3Matches", "exact child F3 lineage gate", errors)

    if errors:
        print("NDS F2 dual-exit contract QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 dual-exit contract QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
