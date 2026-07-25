#!/usr/bin/env python3
"""
Batch validation suite for EXP0013 astro-only execution families.

This tool orchestrates the research-side validation flow:
1. read one deterministic astro feature CSV
2. run one or more family paper executors
3. write one paper journal per family
4. run the signal validator on each journal
5. emit a suite manifest and promotion snapshot
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

from astro_paper_family_runner import FAMILY_DEFAULTS, load_config, run_family  # type: ignore
from astro_signal_validator import family_groups, load_rows, shuffled_baseline, summarize, threshold_grid  # type: ignore


DEFAULT_FAMILIES = ["A0001", "A0002", "A0003", "A0004", "A0005", "A0006", "A0007", "A0090"]


def validate_journal(
    journal_path: Path,
    *,
    entry_threshold: float,
    exit_threshold: float,
    shuffle_rounds: int,
    shuffle_seed: int,
) -> Dict[str, object]:
    rows = load_rows(journal_path)
    return {
        "summary": summarize(rows, entry_threshold=entry_threshold, exit_threshold=exit_threshold),
        "threshold_grid": threshold_grid(rows, [58.0, 62.0, 68.0, 74.0], [48.0, 54.0, 60.0, 66.0]),
        "shuffled_baseline": shuffled_baseline(rows, seed=shuffle_seed, rounds=shuffle_rounds),
        "families": family_groups(rows),
    }


def promotion_snapshot(family: str, report: Dict[str, object]) -> Dict[str, object]:
    summary = report.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    rows = int(summary.get("rows", 0) or 0)
    doctrine_stable = bool(summary.get("doctrine_stability", False))
    schema_stable = bool(summary.get("schema_stability", False))
    entry_hits = int(summary.get("entry_threshold_hits", 0) or 0)
    collisions = int(summary.get("opposite_signal_collisions", 0) or 0)
    avg_hold = float(summary.get("avg_hold_bars", 0.0) or 0.0)
    avg_macro = float(summary.get("avg_macro_timing_score", 0.0) or 0.0)
    avg_minute = float(summary.get("avg_minute_window_score", 0.0) or 0.0)

    decision = "reject_now"
    reasons: List[str] = []
    if rows <= 0:
        reasons.append("empty_journal")
    if not doctrine_stable:
        reasons.append("doctrine_instability")
    if not schema_stable:
        reasons.append("schema_instability")
    if entry_hits <= 0:
        reasons.append("no_entry_hits")
    if collisions > 0:
        reasons.append("opposite_signal_collisions")
    if avg_macro < 50.0:
        reasons.append("weak_macro_timing")
    if avg_minute < 50.0:
        reasons.append("weak_minute_window")

    if rows > 0 and doctrine_stable and schema_stable and entry_hits > 0 and collisions == 0 and avg_macro >= 55.0 and avg_minute >= 55.0:
        decision = "candidate_for_review"
    if decision == "reject_now" and not reasons:
        reasons.append("insufficient_signal_quality")

    return {
        "family": family,
        "decision": decision,
        "reasons": reasons,
        "rows": rows,
        "entry_threshold_hits": entry_hits,
        "avg_hold_bars": avg_hold,
        "avg_macro_timing_score": avg_macro,
        "avg_minute_window_score": avg_minute,
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_suite(
    *,
    csv_path: Path,
    out_dir: Path,
    families: List[str],
    config: Optional[Dict[str, object]],
    entry_threshold: float,
    exit_threshold: float,
    shuffle_rounds: int,
    shuffle_seed: int,
) -> Dict[str, object]:
    journals_dir = out_dir / "journals"
    reports_dir = out_dir / "reports"
    snapshots: List[Dict[str, object]] = []
    manifests: List[Dict[str, object]] = []

    for family in families:
        journal_path = journals_dir / f"{family.lower()}_paper_journal.csv"
        family_run = run_family(csv_path, family, journal_path, config)
        report = validate_journal(
            journal_path,
            entry_threshold=entry_threshold,
            exit_threshold=exit_threshold,
            shuffle_rounds=shuffle_rounds,
            shuffle_seed=shuffle_seed,
        )
        report_path = reports_dir / f"{family.lower()}_validation_report.json"
        write_json(report_path, report)
        snapshot = promotion_snapshot(family, report)
        snapshots.append(snapshot)
        manifests.append(
            {
                "family": family,
                "paper_run": family_run,
                "report_path": str(report_path),
                "journal_path": str(journal_path),
                "promotion_snapshot": snapshot,
            }
        )

    manifest = {
        "csv": str(csv_path),
        "out_dir": str(out_dir),
        "families": manifests,
        "suite_summary": {
            "family_count": len(families),
            "review_candidates": [s["family"] for s in snapshots if s["decision"] == "candidate_for_review"],
            "rejected_now": [s["family"] for s in snapshots if s["decision"] != "candidate_for_review"],
        },
    }
    write_json(out_dir / "suite_manifest.json", manifest)
    write_json(out_dir / "promotion_snapshot.json", snapshots)
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Astro feature CSV produced by astro_feature_builder.py")
    ap.add_argument("--out-dir", required=True, help="Directory for journals and reports")
    ap.add_argument("--config", default="", help="Optional doctrine/threshold config JSON")
    ap.add_argument("--families", nargs="+", default=DEFAULT_FAMILIES, choices=sorted(FAMILY_DEFAULTS.keys()))
    ap.add_argument("--entry-threshold", type=float, default=68.0)
    ap.add_argument("--exit-threshold", type=float, default=60.0)
    ap.add_argument("--shuffle-rounds", type=int, default=200)
    ap.add_argument("--shuffle-seed", type=int, default=13)
    args = ap.parse_args()

    config = load_config(args.config) if args.config else None
    manifest = run_suite(
        csv_path=Path(args.csv),
        out_dir=Path(args.out_dir),
        families=args.families,
        config=config,
        entry_threshold=args.entry_threshold,
        exit_threshold=args.exit_threshold,
        shuffle_rounds=args.shuffle_rounds,
        shuffle_seed=args.shuffle_seed,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
