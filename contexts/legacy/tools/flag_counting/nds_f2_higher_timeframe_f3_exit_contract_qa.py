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
    "manager": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2F3ExitManager.mqh",
    "engine": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/15_higher_timeframe_f3_flag_retest_exit.md",
    "obsidian": ROOT / "docs/obsidian_hook/08_entry_execution/NDS F2 Higher-Timeframe F3 Flag-Retest Exit.md",
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
        print("NDS F2 higher-timeframe F3 exit QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    setup = content["setup"]
    adapter = content["adapter"]
    rules = content["rules"]
    manager = content["manager"]
    engine = content["engine"]
    doc = content["doc"]
    obsidian = content["obsidian"]

    require(expert, '#property version   "2.10"', "expert version", errors)
    require(expert, "FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST", "third exit mode documentation", errors)
    require(expert, "InpF2BTF3ExitHigherTimeframe = PERIOD_H1", "default H1 exit timeframe", errors)
    require(expert, "cfg.higher_timeframe_f3_exit_timeframe = InpF2BTF3ExitHigherTimeframe", "exit timeframe wiring", errors)
    require(expert, "FP_NDSF2ExitModeUsesEntryTimeframeF3(InpF2BTExitMode)", "local-only entry-TF F3 scan", errors)
    require(expert, "PeriodSeconds(resolved_exit_tf) <= PeriodSeconds(_Period)", "strictly-higher timeframe validation", errors)

    require(types, "NDS-F2-WAIST-BREAK-12", "contract version", errors)
    require(types, "nds_f2_waist_break_point2_v12", "schema version", errors)
    require(types, "FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST = 2", "HTF F3 enum", errors)
    require(types, "higher_timeframe_f3_exit_timeframe", "HTF exit config field", errors)
    for token in (
        "dynamic_exit_timeframe",
        "position_open_time",
        "htf_f3_leg1_captured",
        "htf_f3_leg1_node_id",
        "htf_f3_waist_node_id",
        "htf_search_after_time",
    ):
        require(types, token, f"per-trade HTF field {token}", errors)

    require(adapter, "cfg.require_canonical_f3_spawn_for_local_exit", "explicit local-F3 spawn gate", errors)
    require(expert, "InpF2BTRequireCanonicalF3SpawnForLocalExit = true", "explicit local-F3 spawn input", errors)
    forbid(setup, "FP_NDSF2ExitModeIsDynamic(cfg.exit_mode) &&\n      !f2.f2_size_gate_passed", "HTF mode forced through local F2 spawn gate", errors)
    require(rules, "FP_NDSF2ExitModeIsDynamic(cfg.exit_mode)", "dynamic context registration for both modes", errors)

    for token in (
        "FP_NDSF2RefreshHigherTimeframeF3ExitEvents",
        "FP_NDSF2HigherTimeframeF3CandidateEligible",
        "FP_NDSF2HigherTimeframeF3IdentityMatches",
        "FP_NDSF2CaptureHigherTimeframeF3Leg1",
        "FP_NDSF2UpdateHigherTimeframeF3Exit",
        "FP_NDSF2ResetHigherTimeframeF3Candidate",
    ):
        require(manager, token, f"HTF manager function {token}", errors)

    require(manager, "f3.direction != ctx.direction", "same-direction gate", errors)
    require(manager, "f3.leg1.time_anchor <= ctx.htf_search_after_time", "per-position temporal gate", errors)
    require(manager, "f3.leg1.id != ctx.htf_f3_leg1_node_id", "stable Leg1 identity", errors)
    require(manager, "f3.pos_waist <= f3.pos_leg1", "same-F3 Waist correction gate", errors)
    require(manager, "htf_f3_leg1_price", "HTF Leg1 target source", errors)
    require(manager, "ctx.position_ticket", "per-ticket management", errors)
    require(manager, "detector_cfg.show_invalidated_in_audit = true", "candidate invalidation visibility", errors)
    require(manager, "g_fp_nds_f2_htf_f3_exit_cache_open_bar", "once-per-HTF-bar cache", errors)

    require(engine, "FP_NDSF2UpdateHigherTimeframeF3Exit(symbol, trade_cfg, htf_cfg)", "engine HTF exit update", errors)
    require(engine, "FP_NDSF2ExitModeUsesEntryTimeframeF3(trade_cfg.exit_mode)", "no lower-TF F3 scan for HTF mode", errors)

    require(doc, "RR Reference Target = original lower-timeframe F2 Leg2 endpoint", "RR invariance", errors)
    require(doc, "Position Ticket", "per-position traceability", errors)
    require(doc, "exact F3 Waist", "same-F3 correction authority", errors)
    require(obsidian, "PERIOD_H1", "Obsidian H1 default", errors)

    runtime = "\n".join((expert, types, setup, manager, engine))
    for token in ("Print(", "PrintFormat(", "FileOpen(", "ObjectCreate("):
        forbid(runtime, token, f"runtime side effect {token}", errors)
    forbid(rules, "Print(", "runtime Print in rules", errors)
    forbid(rules, "PrintFormat(", "runtime PrintFormat in rules", errors)
    require(rules, "if(!cfg.enable_funnel_diagnostics) return;", "diagnostics opt-in guard", errors)

    if errors:
        print("NDS F2 higher-timeframe F3 exit QA: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("NDS F2 higher-timeframe F3 exit QA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
