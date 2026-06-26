#!/usr/bin/env python3
"""
Calibrate the astro-only final entry surface from veto reasons and profile runs.

This tool does not use price. It inspects:
- family-gated bar consensus
- purity veto reasons
- strict / balanced / probe profiles

and produces a compact recommendation surface for threshold tuning.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

from astro_final_entry_report import (  # type: ignore
    DEFAULT_FAMILIES,
    PURITY_PROFILES,
    build_final_windows,
    decide_bar,
    resolve_family_weights,
)
from astro_paper_family_runner import load_config  # type: ignore
from astro_pure_entry_excel import compute_records, iter_rows, resolve_report_thresholds  # type: ignore


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def profile_run(rows: List[dict], families: List[str], profile_name: str, config: Optional[Dict[str, object]]) -> Dict[str, object]:
    profile = dict(PURITY_PROFILES[profile_name])
    family_weights = resolve_family_weights(profile_name)
    family_records = {
        family: compute_records(rows, family, resolve_report_thresholds(family, config))
        for family in families
    }
    bar_rows = [decide_bar(row, family_records, index, profile, family_weights) for index, row in enumerate(rows)]
    final_windows = build_final_windows(bar_rows)
    veto_counts = Counter()
    for row in bar_rows:
        for reason in (row.get("veto_reason", "") or "").split(","):
            reason = reason.strip()
            if reason:
                veto_counts[reason] += 1

    return {
        "profile": profile_name,
        "profile_params": profile,
        "rows_scanned": len(rows),
        "pure_entry_bars": sum(1 for row in bar_rows if row["purity_state"] == "pure_entry"),
        "probe_bars": sum(1 for row in bar_rows if row["purity_state"] == "probe"),
        "blocked_bars": sum(1 for row in bar_rows if row["purity_state"] == "blocked"),
        "enter_long_bars": sum(1 for row in bar_rows if row["decision"] == "enter_long"),
        "enter_short_bars": sum(1 for row in bar_rows if row["decision"] == "enter_short"),
        "final_entry_windows": len(final_windows),
        "veto_counts": dict(veto_counts.most_common()),
    }


def recommendations(profile_reports: List[Dict[str, object]]) -> Dict[str, object]:
    strict = next((report for report in profile_reports if report["profile"] == "pure_strict"), None)
    balanced = next((report for report in profile_reports if report["profile"] == "pure_balanced"), None)
    probe = next((report for report in profile_reports if report["profile"] == "pure_probe"), None)

    selected = "pure_strict"
    reason = "strict_has_entries"
    if strict and int(strict.get("pure_entry_bars", 0) or 0) <= 0:
        if balanced and int(balanced.get("pure_entry_bars", 0) or 0) > 0:
            selected = "pure_balanced"
            reason = "strict_zero_entries_balanced_has_entries"
        elif probe and int(probe.get("pure_entry_bars", 0) or 0) > 0:
            selected = "pure_probe"
            reason = "strict_and_balanced_zero_entries_probe_has_entries"
        else:
            selected = "pure_strict"
            reason = "all_profiles_zero_entries_keep_strict_for_purity"

    top_vetoes = {}
    if strict:
        top_vetoes = dict(Counter(strict.get("veto_counts", {})).most_common(5))

    overrides: Dict[str, float] = {}
    veto_map = strict.get("veto_counts", {}) if strict else {}
    if isinstance(veto_map, dict):
        if int(veto_map.get("minute_window_low", 0) or 0) > 0:
            overrides["min_minute_window"] = max(55.0, PURITY_PROFILES["pure_strict"]["min_minute_window"] - 2.0)
        if int(veto_map.get("macro_timing_low", 0) or 0) > 0:
            overrides["min_macro_timing"] = max(56.0, PURITY_PROFILES["pure_strict"]["min_macro_timing"] - 2.0)
        if int(veto_map.get("meso_timing_low", 0) or 0) > 0:
            overrides["min_meso_timing"] = max(52.0, PURITY_PROFILES["pure_strict"]["min_meso_timing"] - 2.0)
        if int(veto_map.get("micro_timing_low", 0) or 0) > 0:
            overrides["min_micro_timing"] = max(52.0, PURITY_PROFILES["pure_strict"]["min_micro_timing"] - 2.0)
        if int(veto_map.get("direction_conflict", 0) or 0) > 0:
            overrides["max_direction_conflict_weight"] = min(1.35, PURITY_PROFILES["pure_strict"]["max_direction_conflict_weight"] + 0.1)

    return {
        "recommended_profile": selected,
        "recommendation_reason": reason,
        "strict_top_vetoes": top_vetoes,
        "suggested_overrides": overrides,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrate the pure astro final-entry surface from veto reasons")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--config", default="")
    parser.add_argument("--families", nargs="+", default=DEFAULT_FAMILIES)
    parser.add_argument("--profiles", nargs="+", default=["pure_strict", "pure_balanced", "pure_probe"], choices=sorted(PURITY_PROFILES.keys()))
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"Input CSV not found: {csv_path}")

    config: Optional[Dict[str, object]] = load_config(args.config) if args.config else None
    rows = list(iter_rows(csv_path))
    reports = [profile_run(rows, args.families, profile_name, config) for profile_name in args.profiles]
    payload = {
        "input_csv": str(csv_path),
        "families": args.families,
        "profiles": reports,
        "recommendations": recommendations(reports),
    }
    write_json(Path(args.out_json), payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
