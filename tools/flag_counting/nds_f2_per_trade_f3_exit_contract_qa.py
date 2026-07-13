from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "expert": ROOT / "mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5",
    "types": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh",
    "setup": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBreakSetupRules.mqh",
    "manager": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2F3ExitManager.mqh",
    "detector": ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSF2FastDetector.mqh",
    "doc": ROOT / "docs/nds_entry_architecture/f2_waist_break_point2_limit/14_exact_per_trade_f3_lineage_exit.md",
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
        print("NDS F2 per-trade F3 exit QA: FAIL")
        for error in errors: print(f"- {error}")
        return 1

    expert = content["expert"]
    types = content["types"]
    setup = content["setup"]
    manager = content["manager"]
    detector = content["detector"]
    doc = content["doc"]

    require(expert, '#property version   "2.00"', "expert version", errors)
    require(expert, 'nds_f2_waist_break_point2_v11', "schema identity", errors)
    require(expert, 'cfg.scan_f3 = FP_NDSF2ExitModeUsesEntryTimeframeF3(InpF2BTExitMode)', "mode-aware F3 scan", errors)
    require(expert, 'cfg.f3_show_live_body_candidates', "live child F3 candidates", errors)

    for token in (
        'source_f1_event_id', 'source_f2_event_id', 'source_sequence_id',
        'source_f2_parent_event_id', 'source_f2_origin_node_id',
        'source_f2_waist_node_id', 'exact_child_f3_event_id',
        'exact_child_f3_leg1_node_id', 'exact_child_f3_waist_node_id',
    ):
        require(types, token, f"lineage field {token}", errors)

    require(setup, 'setup.f2_parent_event_id = f2.parent_event_id', "source parent capture", errors)
    require(setup, 'setup.f2_origin_node_id = f2.origin.id', "source origin node capture", errors)
    require(setup, 'setup.f2_waist_node_id = f2.waist.id', "source waist node capture", errors)

    require(manager, 'FP_NDSF2ExactSourceF2Matches', "exact source F2 matcher", errors)
    require(manager, 'FP_NDSF2ExactParentF1Matches', "exact parent F1 matcher", errors)
    require(manager, 'FP_NDSF2ExactChildF3Matches', "exact child F3 matcher", errors)
    require(manager, 'f3.parent_event_id != source_f2.event_id', "direct parent condition", errors)
    require(manager, 'f3.leg1.id != source_f2.confirm.id', "F3 Leg1/F2 confirm identity", errors)
    require(manager, 'child_f3.has_waist', "same-child correction gate", errors)
    require(manager, 'child_f3.leg1.price', "same-child target", errors)
    require(manager, 'child_f3_index = -2', "ambiguous child fail closed", errors)
    forbid(manager, 'events[best].confirm.price', "shared best-F2 target lookup", errors)
    forbid(manager, 'FP_NDSF2DynamicCorrectionSeen', "generic tick correction gate", errors)

    require(detector, 'direct child F3 lifecycle', "detector scope documentation", errors)
    require(doc, 'Position Ticket', "traceability position ticket", errors)
    require(doc, 'Direct Child F3', "traceability direct child F3", errors)
    require(doc, 'No cross-context borrowing', "cross-context prohibition", errors)

    runtime = "\n".join((expert, types, setup, manager, detector))
    for token in ('Print(', 'PrintFormat(', 'FileOpen(', 'ObjectCreate('):
        forbid(runtime, token, f"runtime side effect {token}", errors)

    if errors:
        print("NDS F2 per-trade F3 exit QA: FAIL")
        for error in errors: print(f"- {error}")
        return 1
    print("NDS F2 per-trade F3 exit QA: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
