#!/usr/bin/env python3
"""
EXP0017 Phase 12 — Python Research Workbench

Reads Phase 10 / Phase 11 CSV outputs and produces research-only diagnostics:
- data audit
- out-of-sample leaderboard
- bucket stability analysis
- feature drift analysis
- compact HTML report
- markdown research summary

No broker connectivity. No order placement. No strategy mutation.
"""
from __future__ import annotations

import argparse
import csv
import html
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


def as_float(value: str, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: str, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path, max_rows: int = 1_000_000) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    rows: List[Dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
    return rows


def write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: Optional[List[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        field_order: List[str] = []
        seen = set()
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    seen.add(key)
                    field_order.append(key)
        fieldnames = field_order
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def stdev(values: Iterable[float]) -> float:
    values = list(values)
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values)


def pct(numer: float, denom: float) -> float:
    return 100.0 * numer / denom if denom else 0.0


@dataclass
class WorkbenchConfig:
    data_dir: Path
    out_dir: Path
    phase10_dataset: str = "EXP0017_Phase10_Model_Dataset.csv"
    phase11_predictions: str = "EXP0017_Phase11_Predictions.csv"
    phase11_fold_metrics: str = "EXP0017_Phase11_Fold_Metrics.csv"
    phase11_bucket_validation: str = "EXP0017_Phase11_Bucket_Validation.csv"
    min_oos_samples: int = 20
    min_folds_for_stability: int = 3


@dataclass
class ResearchOutputs:
    data_audit: List[Dict[str, object]] = field(default_factory=list)
    oos_leaderboard: List[Dict[str, object]] = field(default_factory=list)
    bucket_stability: List[Dict[str, object]] = field(default_factory=list)
    feature_drift: List[Dict[str, object]] = field(default_factory=list)
    fold_health: List[Dict[str, object]] = field(default_factory=list)
    summary_lines: List[str] = field(default_factory=list)


def audit_file(name: str, path: Path, rows: List[Dict[str, str]]) -> Dict[str, object]:
    columns = list(rows[0].keys()) if rows else []
    return {
        "logical_name": name,
        "file_name": path.name,
        "exists": path.exists(),
        "row_count": len(rows),
        "column_count": len(columns),
        "first_20_columns": ",".join(columns[:20]),
        "status": "ok" if rows else ("missing" if not path.exists() else "empty"),
    }


def build_bucket_key(row: Dict[str, str]) -> str:
    for key in ("bucket_key", "cg_direction_role_key", "group_direction_role", "group_direction_role_key"):
        if row.get(key):
            return row[key]
    group = row.get("group") or row.get("group_name") or "NA_CG"
    direction = row.get("direction") or "NA_DIRECTION"
    role = row.get("role_key") or f"{row.get('hunter_symbol','NA')}_hunter__{row.get('clean_symbol','NA')}_clean"
    return f"{group}|{direction}|{role}"


def analyze_oos_predictions(pred_rows: List[Dict[str, str]], min_samples: int) -> List[Dict[str, object]]:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in pred_rows:
        key = build_bucket_key(row)
        grouped[key].append(row)

    out: List[Dict[str, object]] = []
    for key, rows in grouped.items():
        actual_r = [as_float(r.get("actual_r") or r.get("primary_r") or r.get("actual_primary_r")) for r in rows]
        actual_win = [1 if as_float(r.get("actual_r") or r.get("primary_r") or r.get("actual_primary_r")) > 0 else 0 for r in rows]
        predicted_r = [as_float(r.get("predicted_avg_r") or r.get("train_avg_r")) for r in rows]
        stop_states = [as_int(r.get("actual_stopped") or r.get("label_stopped_intraday")) for r in rows]
        folds = sorted(set(r.get("fold_id", "") for r in rows if r.get("fold_id", "") != ""))
        sample_count = len(rows)
        avg_actual_r = mean(actual_r)
        row = {
            "bucket_key": key,
            "sample_count": sample_count,
            "fold_count": len(folds),
            "avg_oos_r": round(avg_actual_r, 6),
            "median_proxy_oos_r": round(sorted(actual_r)[len(actual_r)//2] if actual_r else 0.0, 6),
            "win_rate_percent": round(pct(sum(actual_win), len(actual_win)), 3),
            "stop_rate_percent": round(pct(sum(stop_states), len(stop_states)), 3),
            "avg_predicted_r": round(mean(predicted_r), 6),
            "prediction_error_r": round(avg_actual_r - mean(predicted_r), 6),
            "oos_r_stdev": round(stdev(actual_r), 6),
            "eligible": sample_count >= min_samples,
            "research_class": "candidate" if sample_count >= min_samples and avg_actual_r > 0 else "weak_or_insufficient",
        }
        out.append(row)
    out.sort(key=lambda x: (bool(x["eligible"]), float(x["avg_oos_r"]), int(x["sample_count"])), reverse=True)
    return out


def analyze_bucket_stability(pred_rows: List[Dict[str, str]], min_folds: int) -> List[Dict[str, object]]:
    by_bucket_fold: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    for row in pred_rows:
        key = build_bucket_key(row)
        fold = row.get("fold_id", "NA")
        actual_r = as_float(row.get("actual_r") or row.get("primary_r") or row.get("actual_primary_r"))
        by_bucket_fold[(key, fold)].append(actual_r)

    per_bucket: Dict[str, List[float]] = defaultdict(list)
    for (key, _fold), values in by_bucket_fold.items():
        per_bucket[key].append(mean(values))

    out: List[Dict[str, object]] = []
    for key, fold_means in per_bucket.items():
        positive_folds = sum(1 for v in fold_means if v > 0)
        fold_count = len(fold_means)
        avg_fold_r = mean(fold_means)
        stability_score = pct(positive_folds, fold_count) - min(50.0, stdev(fold_means) * 25.0)
        out.append({
            "bucket_key": key,
            "fold_count": fold_count,
            "positive_fold_count": positive_folds,
            "positive_fold_rate_percent": round(pct(positive_folds, fold_count), 3),
            "avg_fold_r": round(avg_fold_r, 6),
            "fold_r_stdev": round(stdev(fold_means), 6),
            "stability_score": round(stability_score, 6),
            "eligible": fold_count >= min_folds,
            "stability_class": "stable_candidate" if fold_count >= min_folds and avg_fold_r > 0 and pct(positive_folds, fold_count) >= 55 else "unstable_or_insufficient",
        })
    out.sort(key=lambda x: (bool(x["eligible"]), float(x["stability_score"]), float(x["avg_fold_r"])), reverse=True)
    return out


def analyze_feature_drift(dataset_rows: List[Dict[str, str]], pred_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    numeric_features = [
        "stop_points", "daily_range_points", "risk_to_daily_range", "reference_age_cycles",
        "hour_ny", "minute_of_day_ny", "cg_quality_score", "cg_direction_role_quality_score",
    ]
    out: List[Dict[str, object]] = []
    for feature in numeric_features:
        dataset_values = [as_float(r.get(feature)) for r in dataset_rows if r.get(feature, "") != ""]
        test_values = [as_float(r.get(feature)) for r in pred_rows if r.get(feature, "") != ""]
        if not dataset_values and not test_values:
            continue
        out.append({
            "feature": feature,
            "dataset_count": len(dataset_values),
            "prediction_count": len(test_values),
            "dataset_mean": round(mean(dataset_values), 6),
            "prediction_mean": round(mean(test_values), 6),
            "mean_delta": round(mean(test_values) - mean(dataset_values), 6),
            "dataset_stdev": round(stdev(dataset_values), 6),
            "prediction_stdev": round(stdev(test_values), 6),
            "drift_note": "large_mean_delta" if abs(mean(test_values) - mean(dataset_values)) > stdev(dataset_values) and len(dataset_values) > 2 else "normal_or_unproven",
        })
    return out


def analyze_fold_health(fold_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    out = []
    for row in fold_rows:
        train = as_int(row.get("train_count") or row.get("train_rows"))
        test = as_int(row.get("test_count") or row.get("test_rows"))
        avg_r = as_float(row.get("test_avg_r") or row.get("avg_test_r") or row.get("avg_actual_r"))
        win_rate = as_float(row.get("test_win_rate_percent") or row.get("win_rate_percent"))
        out.append({
            "fold_id": row.get("fold_id", ""),
            "train_count": train,
            "test_count": test,
            "test_avg_r": round(avg_r, 6),
            "test_win_rate_percent": round(win_rate, 3),
            "status": "usable" if train > 0 and test > 0 else "incomplete",
        })
    return out


def build_html_report(outputs: ResearchOutputs, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    def table(rows: List[Dict[str, object]], limit: int = 40) -> str:
        if not rows:
            return "<p>No rows.</p>"
        headers = list(rows[0].keys())
        body = ["<table><thead><tr>" + "".join(f"<th>{html.escape(str(h))}</th>" for h in headers) + "</tr></thead><tbody>"]
        for row in rows[:limit]:
            body.append("<tr>" + "".join(f"<td>{html.escape(str(row.get(h, '')))}</td>" for h in headers) + "</tr>")
        body.append("</tbody></table>")
        return "\n".join(body)

    doc = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>EXP0017 Phase 12 Research Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; background: #111; color: #eee; }}
h1,h2 {{ color: #fff; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 28px; font-size: 12px; }}
th,td {{ border: 1px solid #444; padding: 6px; vertical-align: top; }}
th {{ background: #222; }}
tr:nth-child(even) {{ background: #181818; }}
.badge {{ display: inline-block; padding: 4px 8px; background: #222; border: 1px solid #444; margin: 2px; }}
</style></head><body>
<h1>EXP0017 Phase 12 — Python Research Workbench</h1>
<p><b>Boundary:</b> research only; no trade, no execution, no mutation.</p>
<h2>Data Audit</h2>{table(outputs.data_audit)}
<h2>Out-of-Sample Leaderboard</h2>{table(outputs.oos_leaderboard)}
<h2>Bucket Stability</h2>{table(outputs.bucket_stability)}
<h2>Feature Drift</h2>{table(outputs.feature_drift)}
<h2>Fold Health</h2>{table(outputs.fold_health)}
</body></html>"""
    output_path.write_text(doc, encoding="utf-8")


def run_workbench(config: WorkbenchConfig) -> ResearchOutputs:
    config.out_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = config.data_dir / config.phase10_dataset
    pred_path = config.data_dir / config.phase11_predictions
    fold_path = config.data_dir / config.phase11_fold_metrics
    bucket_validation_path = config.data_dir / config.phase11_bucket_validation

    dataset_rows = read_csv(dataset_path)
    pred_rows = read_csv(pred_path)
    fold_rows = read_csv(fold_path)
    bucket_validation_rows = read_csv(bucket_validation_path)

    outputs = ResearchOutputs()
    outputs.data_audit = [
        audit_file("phase10_dataset", dataset_path, dataset_rows),
        audit_file("phase11_predictions", pred_path, pred_rows),
        audit_file("phase11_fold_metrics", fold_path, fold_rows),
        audit_file("phase11_bucket_validation", bucket_validation_path, bucket_validation_rows),
    ]
    outputs.oos_leaderboard = analyze_oos_predictions(pred_rows, config.min_oos_samples)
    outputs.bucket_stability = analyze_bucket_stability(pred_rows, config.min_folds_for_stability)
    outputs.feature_drift = analyze_feature_drift(dataset_rows, pred_rows)
    outputs.fold_health = analyze_fold_health(fold_rows)

    write_csv(config.out_dir / "phase12_data_audit.csv", outputs.data_audit)
    write_csv(config.out_dir / "phase12_oos_leaderboard.csv", outputs.oos_leaderboard)
    write_csv(config.out_dir / "phase12_bucket_stability.csv", outputs.bucket_stability)
    write_csv(config.out_dir / "phase12_feature_drift.csv", outputs.feature_drift)
    write_csv(config.out_dir / "phase12_fold_health.csv", outputs.fold_health)
    build_html_report(outputs, config.out_dir / "phase12_html_report.html")

    top = outputs.oos_leaderboard[:10]
    summary = [
        "# EXP0017 Phase 12 Research Summary",
        "",
        "Boundary: research only. No execution, no filtering, no strategy mutation.",
        "",
        f"Dataset rows: {len(dataset_rows)}",
        f"Prediction rows: {len(pred_rows)}",
        f"Fold rows: {len(fold_rows)}",
        "",
        "## Top OOS Buckets",
    ]
    for row in top:
        summary.append(f"- `{row.get('bucket_key')}` — samples={row.get('sample_count')}, avg_oos_r={row.get('avg_oos_r')}, win_rate={row.get('win_rate_percent')}%")
    (config.out_dir / "phase12_research_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    outputs.summary_lines = summary
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="EXP0017 Phase 12 Python research workbench")
    parser.add_argument("--data-dir", default=".", help="Directory containing Phase 10/11 CSV files")
    parser.add_argument("--out-dir", default="research/exp0017_phase12/outputs", help="Output directory for Phase 12 reports")
    parser.add_argument("--min-oos-samples", type=int, default=20)
    parser.add_argument("--min-folds-for-stability", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = WorkbenchConfig(
        data_dir=Path(args.data_dir),
        out_dir=Path(args.out_dir),
        min_oos_samples=args.min_oos_samples,
        min_folds_for_stability=args.min_folds_for_stability,
    )
    outputs = run_workbench(config)
    print("EXP0017 Phase12 research workbench complete")
    print(f"data audit rows: {len(outputs.data_audit)}")
    print(f"leaderboard rows: {len(outputs.oos_leaderboard)}")
    print(f"stability rows: {len(outputs.bucket_stability)}")
    print(f"outputs: {config.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
