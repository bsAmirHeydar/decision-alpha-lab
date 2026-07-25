#!/usr/bin/env python3
"""
Run the final astro-only validation stack on one deterministic CSV.

Outputs:
- family validation suite
- final entry reports for strict / balanced / probe
- purity calibration recommendations
- one finalization manifest
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

from astro_final_entry_report import DEFAULT_FAMILIES, PURITY_PROFILES, main as _unused  # type: ignore
from astro_family_validation_suite import run_suite  # type: ignore
from astro_purity_calibrator import recommendations, profile_run, write_json  # type: ignore
from astro_paper_family_runner import load_config  # type: ignore
from astro_pure_entry_excel import iter_rows  # type: ignore


def final_report_json(
    rows: List[dict],
    families: List[str],
    profiles: List[str],
    config: Optional[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [profile_run(rows, families, profile_name, config) for profile_name in profiles]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full astro-only finalization suite")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--config", default="")
    parser.add_argument("--families", nargs="+", default=DEFAULT_FAMILIES)
    parser.add_argument("--profiles", nargs="+", default=["pure_strict", "pure_balanced", "pure_probe"], choices=sorted(PURITY_PROFILES.keys()))
    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out_dir)
    if not csv_path.exists():
        raise SystemExit(f"Input CSV not found: {csv_path}")

    config: Optional[Dict[str, object]] = load_config(args.config) if args.config else None
    rows = list(iter_rows(csv_path))

    validation_manifest = run_suite(
        csv_path=csv_path,
        out_dir=out_dir / "family_validation",
        families=args.families + ["A0090"] if "A0090" not in args.families else args.families,
        config=config,
        entry_threshold=68.0,
        exit_threshold=60.0,
        shuffle_rounds=200,
        shuffle_seed=13,
    )
    profile_reports = final_report_json(rows, args.families, args.profiles, config)
    calibration = recommendations(profile_reports)
    payload = {
        "input_csv": str(csv_path),
        "families": args.families,
        "profiles": profile_reports,
        "calibration": calibration,
        "family_validation_summary": validation_manifest.get("suite_summary", {}),
        "review_candidates": validation_manifest.get("suite_summary", {}).get("review_candidates", []),
        "rejected_now": validation_manifest.get("suite_summary", {}).get("rejected_now", []),
    }
    write_json(out_dir / "finalization_manifest.json", payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
