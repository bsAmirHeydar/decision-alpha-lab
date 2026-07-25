#!/usr/bin/env python3
"""Compare exact-accelerated and full-reference NDS Hook 86.4 tester logs."""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

FIELD_RE = re.compile(r"([A-Za-z0-9_]+)=([^\s]+)")
DECISION_FIELDS = ("action", "status", "setup_key", "entry", "stop", "target")


@dataclass(frozen=True)
class RunRecord:
    line_number: int
    fields: dict[str, str]

    @property
    def decision(self) -> tuple[str, ...]:
        return tuple(self.fields.get(name, "") for name in DECISION_FIELDS)

    @property
    def elapsed_us(self) -> int:
        try:
            return int(self.fields.get("elapsed_us", "0"))
        except ValueError:
            return 0


def parse_runs(path: Path) -> list[RunRecord]:
    records: list[RunRecord] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if "NDS_BT " not in line or "NDS_BT_INIT" in line or "NDS_BT_SESSION" in line:
            continue
        fields = dict(FIELD_RE.findall(line))
        if "action" not in fields or "elapsed_us" not in fields:
            continue
        records.append(RunRecord(line_number=line_number, fields=fields))
    return records


def timing_summary(records: list[RunRecord]) -> dict[str, float | int]:
    samples = [record.elapsed_us for record in records if record.elapsed_us > 0]
    if not samples:
        return {"samples": 0, "total_us": 0, "mean_us": 0.0, "median_us": 0.0, "max_us": 0}
    return {
        "samples": len(samples),
        "total_us": sum(samples),
        "mean_us": statistics.fmean(samples),
        "median_us": statistics.median(samples),
        "max_us": max(samples),
    }


def compare(exact: list[RunRecord], reference: list[RunRecord]) -> tuple[list[dict[str, object]], dict[str, object]]:
    mismatches: list[dict[str, object]] = []
    common = min(len(exact), len(reference))
    for index in range(common):
        if exact[index].decision == reference[index].decision:
            continue
        mismatches.append(
            {
                "run": index + 1,
                "exact_line": exact[index].line_number,
                "reference_line": reference[index].line_number,
                "exact": dict(zip(DECISION_FIELDS, exact[index].decision)),
                "reference": dict(zip(DECISION_FIELDS, reference[index].decision)),
            }
        )
    if len(exact) != len(reference):
        mismatches.append(
            {
                "run_count_mismatch": True,
                "exact_runs": len(exact),
                "reference_runs": len(reference),
            }
        )

    exact_timing = timing_summary(exact)
    reference_timing = timing_summary(reference)
    speedup = 0.0
    reduction_pct = 0.0
    if exact_timing["total_us"] and reference_timing["total_us"]:
        speedup = float(reference_timing["total_us"]) / float(exact_timing["total_us"])
        reduction_pct = (1.0 - float(exact_timing["total_us"]) / float(reference_timing["total_us"])) * 100.0
    summary = {
        "decision_parity": not mismatches,
        "exact_runs": len(exact),
        "reference_runs": len(reference),
        "mismatch_count": len(mismatches),
        "exact_timing": exact_timing,
        "reference_timing": reference_timing,
        "speedup_x": speedup,
        "wall_work_reduction_pct": reduction_pct,
    }
    return mismatches, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("exact_log", type=Path)
    parser.add_argument("reference_log", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    exact = parse_runs(args.exact_log)
    reference = parse_runs(args.reference_log)
    mismatches, summary = compare(exact, reference)
    payload = {"summary": summary, "mismatches": mismatches}

    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.json_path:
        args.json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not exact or not reference:
        print("ERROR: both logs must contain NDS_BT run lines with action and elapsed_us", file=sys.stderr)
        return 2
    return 0 if summary["decision_parity"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
