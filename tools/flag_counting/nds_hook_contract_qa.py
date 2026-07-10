#!/usr/bin/env python3
"""Static contract QA for the NDS Hook pre-canon baseline.

The scanner intentionally validates only decisions that are already locked in
repository doctrine. It does not encode unresolved questionnaire answers such
as the final ownership-window size, rebound evidence, or Zone boundaries.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Check:
    check_id: str
    status: str
    path: str
    detail: str


REQUIRED_FILES = (
    "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5",
    "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh",
    "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh",
    "docs/nds_hook_architecture/65_phase48_post_f3_hook_recognition_doctrine.md",
    "docs/nds_hook_architecture/66_phase49_post_f3_recognition_code_step7.md",
    "docs/hook_validity/HOOK-VAL-0001_Valid_Hook_Philosophy_and_Filtering_Policy.md",
    "docs/hook_validity/HOOK-VAL-0002_Hook_After_Hook_Chained_Node_Architecture.md",
    "docs/hook_validity/HOOK-VAL-0003_Hook_After_Opposing_F3_Architecture.md",
)


def read(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="ignore")


def contains(checks: list[Check], root: Path, rel: str, needle: str, check_id: str, detail: str) -> None:
    text = read(root, rel)
    ok = needle in text
    checks.append(Check(check_id, "PASS" if ok else "FAIL", rel, detail))


def excludes(checks: list[Check], root: Path, rel: str, needle: str, check_id: str, detail: str) -> None:
    text = read(root, rel)
    ok = needle not in text
    checks.append(Check(check_id, "PASS" if ok else "FAIL", rel, detail))


def run(root: Path) -> list[Check]:
    checks: list[Check] = []

    for rel in REQUIRED_FILES:
        ok = (root / rel).is_file()
        checks.append(Check("NDS_REQUIRED_FILE", "PASS" if ok else "FAIL", rel, "required NDS authority or implementation file"))

    rules = "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh"
    types = "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh"
    export = "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh"
    ea = "mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5"

    contains(checks, root, rules, "FP_HookP02BarWithinBarsAfter", "NDS_BAR_INDEX_WINDOW",
             "post-F3 ownership window uses canonical bar indexes")
    excludes(checks, root, rules, "PeriodSeconds(_Period)", "NDS_NO_WALL_CLOCK_OWNERSHIP",
             "post-F3 structural ownership is not derived from chart-period seconds")
    contains(checks, root, rules, "cfg.valid_f3_require_opposite_direction", "NDS_DIRECTION_INPUT_LIVE",
             "opposite-direction strictness input is consumed by recognition logic")
    contains(checks, root, rules, "cfg.post_f3_selection_priority == FP_HOOK_POST_F3_PRIORITY_EARLIEST_FIRST",
             "NDS_EARLIEST_PRIORITY_LIVE", "EARLIEST_FIRST has an explicit comparator branch")
    contains(checks, root, rules, "candidate.origin_bar_index < current.origin_bar_index",
             "NDS_EARLIEST_USES_BAR_INDEX", "earliest selection compares canonical origin bar indexes")
    contains(checks, root, rules, "opposing_f3_terminal_bar_index", "NDS_OWNERSHIP_TRACE_STATE",
             "selected F3 terminal bar is preserved on the Hook sequence")
    contains(checks, root, export, "post_f3_structural_axis", "NDS_SUMMARY_AXIS_AUDIT",
             "summary export declares the structural axis")
    contains(checks, root, export, "post_f3_origin_distance_bars", "NDS_SEQUENCE_DISTANCE_AUDIT",
             "sequence export preserves F3-to-Hook distance in bars")
    contains(checks, root, types, 'FP_HOOK_P02_SCHEMA_VERSION "hook_phase02_sequences_v2"',
             "NDS_SCHEMA_BUMP", "audit schema is versioned after adding ownership fields")
    contains(checks, root, ea, "InpHookPhase02ShowOnlyValidHooks = true", "NDS_VALID_ONLY_DEFAULT",
             "production Hook view remains valid-only by default")
    contains(checks, root, ea, '#property version   "18.30"', "NDS_EA_VERSION",
             "central Phoenix EA carries the NDS entry-transition version")

    # The Hook module remains analysis/visualization only. The exact word may
    # appear elsewhere in the large central EA, so scan only Hook Phase02 files.
    hook_scope = "\n".join(read(root, rel) for rel in (rules, types, export))
    forbidden = ("OrderSend(", "CTrade", "trade.Buy(", "trade.Sell(")
    for token in forbidden:
        checks.append(Check("NDS_NO_EXECUTION_IN_HOOK_P02", "PASS" if token not in hook_scope else "FAIL",
                            "mql5/Include/FlagCountingPhoenix/FP_HookPhase02*.mqh",
                            f"Hook Phase02 excludes execution token {token}"))

    if not any(c.status == "FAIL" for c in checks):
        checks.append(Check("NDS_HOOK_CONTRACT_QA", "PASS", ".", "all locked pre-canon contract checks passed"))
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
