#!/usr/bin/env python3
"""EXP0017 Phase 12.5 — Pipeline Integrity & Schema Reconciliation.

Deep, deterministic, standard-library audit of Phase 07 through Phase 12 outputs.
It verifies file contracts, primary keys, cross-phase lineage, semantic invariants,
walk-forward temporal boundaries, writer summaries, and Phase 13 readiness.

Research boundary: no broker connectivity, no order placement, no signal filtering,
no strategy mutation, and no production model promotion.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


def parse_dt(value: str) -> Optional[datetime]:
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def as_float(value: object, default: float = 0.0) -> float:
    try:
        text = "" if value is None else str(value).strip()
        return default if text == "" else float(text)
    except (TypeError, ValueError):
        return default


def as_int(value: object, default: int = 0) -> int:
    try:
        text = "" if value is None else str(value).strip()
        return default if text == "" else int(float(text))
    except (TypeError, ValueError):
        return default


def as_bool(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "on"}


def read_csv(path: Path, max_rows: int) -> Tuple[List[Dict[str, str]], List[str], Optional[str]]:
    if not path.exists():
        return [], [], "missing"
    try:
        rows: List[Dict[str, str]] = []
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers = list(reader.fieldnames or [])
            for index, row in enumerate(reader):
                if index >= max_rows:
                    break
                rows.append({str(k): ("" if v is None else str(v)) for k, v in row.items() if k is not None})
        return rows, headers, None
    except (OSError, csv.Error, UnicodeError) as exc:
        return [], [], f"read_error:{exc}"


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        order: List[str] = []
        seen: Set[str] = set()
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    seen.add(key)
                    order.append(key)
        fieldnames = order or ["status"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def composite_key(row: Mapping[str, str], columns: Sequence[str]) -> str:
    return "||".join((row.get(c) or "").strip() for c in columns)


def safe_pct(n: int, d: int) -> float:
    return 100.0 * n / d if d else 0.0


@dataclass(frozen=True)
class FileContract:
    phase: str
    logical_name: str
    filename: str
    required: bool
    required_columns: Tuple[str, ...]
    primary_key: Tuple[str, ...] = ()
    timestamp_columns: Tuple[str, ...] = ()


@dataclass
class Config:
    data_dir: Path
    out_dir: Path
    max_rows: int = 500_000
    exact_lineage_min_pct: float = 99.90
    count_tolerance: int = 0
    fail_on_warning: bool = False
    filenames: Dict[str, str] = field(default_factory=dict)


def contracts(cfg: Config) -> List[FileContract]:
    f = cfg.filenames
    return [
        FileContract("07", "outcome_study", f["p07"], True,
            ("outcome_id","signal_id","availability","group","group_minutes","current_cycle","reference_cycle","direction","side","clean_symbol","hunter_symbol","confirmation_ny","entry_price","stop_price","stop_points","cycle_end_r","mfe_r","mae_r","stop_hit_intraday","daily_range_points"),
            ("outcome_id",), ("confirmation_ny",)),
        FileContract("08", "overall_statistics", f["p08_overall"], True,
            ("dimension","key","sample_count","win_count","loss_count","win_rate_percent","stop_count","stop_rate_percent","max_stop_streak","avg_r"),
            ("dimension","key")),
        FileContract("08", "cg_direction_role_statistics", f["p08_cgdr"], True,
            ("dimension","key","sample_count","win_rate_percent","stop_rate_percent","avg_r","avg_normalized","avg_mfe_r","avg_mae_r"),
            ("dimension","key")),
        FileContract("09", "rankings_all", f["p09_rank"], True,
            ("rank","report_name","bucket_key","sample_count","win_rate_percent","avg_r","quality_score","grade","shortlist","red_flags"),
            ("report_name","bucket_key")),
        FileContract("09", "shortlist", f["p09_short"], False,
            ("rank","report_name","bucket_key","sample_count","avg_r","quality_score","grade","shortlist"),
            ("report_name","bucket_key")),
        FileContract("10", "model_dataset", f["p10"], True,
            ("sample_id","outcome_id","signal_id","model_use_status","availability","group","group_minutes","current_cycle","reference_cycle","reference_age_cycles","direction","side","clean_symbol","hunter_symbol","role_key","confirmation_ny","stop_points","daily_range_points","primary_window","primary_r","label_class","label_binary_win","label_stopped_intraday"),
            ("sample_id",), ("confirmation_ny",)),
        FileContract("10", "label_summary", f["p10_summary"], True, ("metric","value"), ("metric",)),
        FileContract("11", "fold_plan", f["p11_fold"], True,
            ("fold_id","train_start","train_end","embargo_start","embargo_end","test_start","test_end","train_count","test_count","usable","status"),
            ("fold_id",), ("train_start","train_end","embargo_start","embargo_end","test_start","test_end")),
        FileContract("11", "predictions", f["p11_pred"], True,
            ("fold_id","sample_id","signal_id","group","direction","role_key","bucket_key","bucket_source","train_count_for_bucket","predicted_avg_r","predicted_win_rate","actual_r","actual_win","actual_loss","actual_stop","model_use_status"),
            ("fold_id","sample_id")),
        FileContract("11", "fold_metrics", f["p11_metrics"], True,
            ("report_name","fold_id","bucket_key","bucket_label","samples","wins","losses","stops","avg_r","win_rate","stop_rate"),
            ("report_name","fold_id","bucket_key")),
        FileContract("11", "bucket_validation", f["p11_bucket"], True,
            ("fold_id","bucket_key","bucket_label","train_count","train_wins","train_losses","train_stops","train_avg_r","train_win_rate","train_stop_rate","edge_class"),
            ("fold_id","bucket_key")),
        FileContract("11", "experiment_summary", f["p11_summary"], True, ("metric","value"), ("metric",)),
    ]


class IntegrityAuditor:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.loaded: Dict[str, List[Dict[str, str]]] = {}
        self.headers: Dict[str, List[str]] = {}
        self.file_audit: List[Dict[str, object]] = []
        self.schema_issues: List[Dict[str, object]] = []
        self.duplicate_report: List[Dict[str, object]] = []
        self.lineage: List[Dict[str, object]] = []
        self.semantic_issues: List[Dict[str, object]] = []
        self.temporal_audit: List[Dict[str, object]] = []
        self.metric_checks: List[Dict[str, object]] = []
        self.gates: List[Dict[str, object]] = []

    def load_and_audit_files(self) -> None:
        for c in contracts(self.cfg):
            path = self.cfg.data_dir / c.filename
            rows, headers, error = read_csv(path, self.cfg.max_rows)
            self.loaded[c.logical_name] = rows
            self.headers[c.logical_name] = headers
            missing = [col for col in c.required_columns if col not in headers]
            duplicate_count = 0
            empty_count = 0
            duplicate_examples: List[str] = []
            if c.primary_key and rows:
                keys = [composite_key(r, c.primary_key) for r in rows]
                empty_count = sum(1 for k in keys if not k.replace("|", "").strip())
                counts = Counter(k for k in keys if k.replace("|", "").strip())
                duplicate_keys = [k for k, n in counts.items() if n > 1]
                duplicate_count = sum(counts[k] - 1 for k in duplicate_keys)
                duplicate_examples = duplicate_keys[:20]
                if duplicate_count:
                    self.duplicate_report.append({
                        "phase": c.phase, "logical_name": c.logical_name, "file_name": c.filename,
                        "primary_key": "|".join(c.primary_key), "duplicate_occurrences": duplicate_count,
                        "duplicate_key_examples": ";".join(duplicate_examples),
                    })
            ts_failures = 0
            for column in c.timestamp_columns:
                if column in headers:
                    ts_failures += sum(1 for r in rows if (r.get(column) or "").strip() and parse_dt(r.get(column, "")) is None)
            status = "ok"
            if error == "missing": status = "missing_required" if c.required else "missing_optional"
            elif error: status = "read_error"
            elif not headers: status = "empty_or_no_header"
            elif missing or empty_count or duplicate_count: status = "failed"
            elif ts_failures: status = "warning"
            self.file_audit.append({
                "phase": c.phase, "logical_name": c.logical_name, "file_name": c.filename,
                "required": c.required, "exists": path.exists(), "row_count_loaded": len(rows),
                "column_count": len(headers), "missing_required_column_count": len(missing),
                "empty_primary_key_count": empty_count, "duplicate_primary_key_occurrences": duplicate_count,
                "timestamp_parse_failures": ts_failures, "status": status, "read_error": error or "",
            })
            if error == "missing":
                self.schema_issues.append({"phase": c.phase,"logical_name": c.logical_name,"file_name": c.filename,
                    "issue_type":"missing_file","column":"","severity":"critical" if c.required else "warning",
                    "detail":"Required upstream output is absent." if c.required else "Optional output is absent."})
            elif error:
                self.schema_issues.append({"phase": c.phase,"logical_name": c.logical_name,"file_name": c.filename,
                    "issue_type":"read_error","column":"","severity":"critical","detail":error})
            for col in missing:
                self.schema_issues.append({"phase": c.phase,"logical_name": c.logical_name,"file_name": c.filename,
                    "issue_type":"missing_required_column","column":col,"severity":"critical","detail":"Column contract mismatch."})
            if empty_count:
                self.schema_issues.append({"phase": c.phase,"logical_name": c.logical_name,"file_name": c.filename,
                    "issue_type":"empty_primary_key","column":"|".join(c.primary_key),"severity":"critical","detail":str(empty_count)})
            if duplicate_count:
                self.schema_issues.append({"phase": c.phase,"logical_name": c.logical_name,"file_name": c.filename,
                    "issue_type":"duplicate_primary_key","column":"|".join(c.primary_key),"severity":"critical","detail":str(duplicate_count)})
            if ts_failures:
                self.schema_issues.append({"phase": c.phase,"logical_name": c.logical_name,"file_name": c.filename,
                    "issue_type":"timestamp_parse_failure","column":"|".join(c.timestamp_columns),"severity":"error","detail":str(ts_failures)})

    def reconcile(self, name: str, parent: str, parent_cols: Sequence[str], child: str, child_cols: Sequence[str], mode: str) -> None:
        p_rows = self.loaded.get(parent, [])
        c_rows = self.loaded.get(child, [])
        p = {composite_key(r, parent_cols) for r in p_rows if composite_key(r, parent_cols).replace("|", "").strip()}
        c = {composite_key(r, child_cols) for r in c_rows if composite_key(r, child_cols).replace("|", "").strip()}
        matched = p & c
        missing = p - c
        orphan = c - p
        parent_cov = safe_pct(len(matched), len(p))
        child_cov = safe_pct(len(matched), len(c))
        if mode == "exact":
            passed = parent_cov >= self.cfg.exact_lineage_min_pct and not orphan
        else:
            passed = not orphan
        self.lineage.append({
            "relation_name": name, "relation_mode": mode, "parent": parent, "parent_key": "|".join(parent_cols),
            "child": child, "child_key": "|".join(child_cols), "parent_unique_keys": len(p),
            "child_unique_keys": len(c), "matched_keys": len(matched), "missing_in_child": len(missing),
            "orphan_in_child": len(orphan), "parent_coverage_percent": round(parent_cov, 6),
            "child_coverage_percent": round(child_cov, 6), "status": "pass" if passed else "fail",
            "missing_examples": ";".join(sorted(missing)[:20]), "orphan_examples": ";".join(sorted(orphan)[:20]),
        })

    def audit_lineage(self) -> None:
        self.reconcile("phase07_outcome_to_phase10_outcome","outcome_study",("outcome_id",),"model_dataset",("outcome_id",),"exact")
        self.reconcile("phase07_signal_to_phase10_signal","outcome_study",("signal_id",),"model_dataset",("signal_id",),"exact")
        self.reconcile("phase10_sample_to_phase11_prediction","model_dataset",("sample_id",),"predictions",("sample_id",),"child_subset")
        self.reconcile("phase10_signal_to_phase11_prediction","model_dataset",("signal_id",),"predictions",("signal_id",),"child_subset")
        self.reconcile("phase11_fold_plan_to_predictions","fold_plan",("fold_id",),"predictions",("fold_id",),"child_subset")
        self.reconcile("phase11_fold_plan_to_bucket_validation","fold_plan",("fold_id",),"bucket_validation",("fold_id",),"child_subset")

    def issue(self, scope: str, key: str, issue_type: str, severity: str, detail: str) -> None:
        self.semantic_issues.append({"scope":scope,"record_key":key,"issue_type":issue_type,"severity":severity,"detail":detail})

    def audit_semantics(self) -> None:
        for r in self.loaded.get("outcome_study", []):
            key = r.get("outcome_id", "")
            direction, side = r.get("direction", "").upper(), r.get("side", "").upper()
            if direction == "BUY" and side != "LOW": self.issue("phase07",key,"buy_side_mismatch","critical",f"side={side}")
            if direction == "SELL" and side != "HIGH": self.issue("phase07",key,"sell_side_mismatch","critical",f"side={side}")
            if r.get("clean_symbol", "") == r.get("hunter_symbol", "") and r.get("clean_symbol", ""):
                self.issue("phase07",key,"clean_equals_hunter","critical",r.get("clean_symbol", ""))
            if r.get("availability", "").upper() == "COMPLETE" and as_float(r.get("stop_points")) <= 0:
                self.issue("phase07",key,"complete_outcome_nonpositive_stop","critical",r.get("stop_points", ""))

        for r in self.loaded.get("model_dataset", []):
            key = r.get("sample_id", "")
            direction, side = r.get("direction", "").upper(), r.get("side", "").upper()
            if direction == "BUY" and side != "LOW": self.issue("phase10",key,"buy_side_mismatch","critical",f"side={side}")
            if direction == "SELL" and side != "HIGH": self.issue("phase10",key,"sell_side_mismatch","critical",f"side={side}")
            if r.get("clean_symbol", "") == r.get("hunter_symbol", "") and r.get("clean_symbol", ""):
                self.issue("phase10",key,"clean_equals_hunter","critical",r.get("clean_symbol", ""))
            if r.get("model_use_status", "").lower() in {"model_ready","ready","usable"} and as_float(r.get("stop_points")) <= 0:
                self.issue("phase10",key,"model_ready_nonpositive_stop","critical",r.get("stop_points", ""))
            label = r.get("label_class", "").upper()
            binary = as_int(r.get("label_binary_win"))
            if label == "WIN" and binary != 1: self.issue("phase10",key,"win_label_binary_mismatch","error",str(binary))
            if label in {"LOSS","FLAT"} and binary != 0: self.issue("phase10",key,"nonwin_label_binary_mismatch","error",str(binary))

        for r in self.loaded.get("predictions", []):
            key = f"{r.get('fold_id','')}||{r.get('sample_id','')}"
            actual_r = as_float(r.get("actual_r"))
            win, loss = as_int(r.get("actual_win")), as_int(r.get("actual_loss"))
            if win and loss: self.issue("phase11",key,"actual_win_and_loss_both_true","critical","")
            if actual_r > 0 and win != 1: self.issue("phase11",key,"positive_r_not_win","error",str(actual_r))
            if actual_r < 0 and loss != 1: self.issue("phase11",key,"negative_r_not_loss","error",str(actual_r))

    def audit_temporal(self) -> None:
        folds = self.loaded.get("fold_plan", [])
        previous_test_end: Optional[datetime] = None
        for r in folds:
            fold = r.get("fold_id", "")
            times = {k: parse_dt(r.get(k, "")) for k in ("train_start","train_end","embargo_start","embargo_end","test_start","test_end")}
            parse_fail = [k for k,v in times.items() if v is None]
            overlap = False
            order_ok = False
            if not parse_fail:
                order_ok = bool(times["train_start"] <= times["train_end"] <= times["embargo_start"] <= times["embargo_end"] <= times["test_start"] <= times["test_end"])
                overlap = not order_ok
            step_overlap = bool(previous_test_end and times.get("test_start") and times["test_start"] < previous_test_end)
            if times.get("test_end"): previous_test_end = times["test_end"]
            status = "pass" if not parse_fail and order_ok else "fail"
            self.temporal_audit.append({
                "fold_id":fold,"parse_failure_columns":";".join(parse_fail),"ordered_boundaries":order_ok,
                "train_test_or_embargo_overlap":overlap,"test_window_overlaps_previous_test":step_overlap,
                "train_count":as_int(r.get("train_count")),"test_count":as_int(r.get("test_count")),
                "usable":as_bool(r.get("usable")),"status":status,
            })

    def metric_map(self, logical: str) -> Dict[str, str]:
        return {(r.get("metric") or "").strip(): (r.get("value") or "").strip() for r in self.loaded.get(logical, [])}

    def metric(self, name: str, left: float, right: float, left_source: str, right_source: str, note: str) -> None:
        delta = left - right
        self.metric_checks.append({"check_name":name,"left_source":left_source,"left_value":left,
            "right_source":right_source,"right_value":right,"delta":delta,"tolerance":self.cfg.count_tolerance,
            "status":"pass" if abs(delta) <= self.cfg.count_tolerance else "fail","note":note})

    def audit_metrics(self) -> None:
        p10s = self.metric_map("label_summary")
        p11s = self.metric_map("experiment_summary")
        if "rows_written" in p10s:
            self.metric("phase10_summary_vs_dataset",as_float(p10s["rows_written"]),len(self.loaded.get("model_dataset", [])),
                        "Phase10 Label Summary rows_written","Phase10 dataset row count","Writer summary must equal materialized rows.")
        if "folds_built" in p11s:
            self.metric("phase11_summary_vs_fold_plan",as_float(p11s["folds_built"]),len(self.loaded.get("fold_plan", [])),
                        "Phase11 summary folds_built","Phase11 fold plan row count","Fold summary must reconcile.")
        if "predictions_written" in p11s:
            self.metric("phase11_summary_vs_predictions",as_float(p11s["predictions_written"]),len(self.loaded.get("predictions", [])),
                        "Phase11 summary predictions_written","Phase11 predictions row count","Prediction summary must reconcile.")
        if "bucket_models_built" in p11s:
            self.metric("phase11_summary_vs_bucket_validation",as_float(p11s["bucket_models_built"]),len(self.loaded.get("bucket_validation", [])),
                        "Phase11 summary bucket_models_built","Phase11 bucket validation row count","Bucket model summary must reconcile.")
        complete = sum(1 for r in self.loaded.get("outcome_study", []) if r.get("availability", "").upper() == "COMPLETE")
        overall = self.loaded.get("overall_statistics", [])
        if overall:
            self.metric("phase07_complete_vs_phase08_overall",complete,as_float(overall[0].get("sample_count")),
                        "Phase07 COMPLETE row count","Phase08 overall sample_count","Only complete tradeable outcomes belong in primary statistics.")

    def gate(self, name: str, required: bool, passed: bool, severity: str, evidence: str, remediation: str) -> None:
        self.gates.append({"gate_name":name,"required":required,"passed":passed,"severity":severity,"evidence":evidence,"remediation":remediation})

    def build_gates(self) -> None:
        missing_required = [r for r in self.file_audit if r["required"] and not r["exists"]]
        critical_schema = [r for r in self.schema_issues if r["severity"] == "critical"]
        duplicates = sum(as_int(r.get("duplicate_occurrences")) for r in self.duplicate_report)
        lineage_fail = [r for r in self.lineage if r["status"] == "fail"]
        semantic_critical = [r for r in self.semantic_issues if r["severity"] == "critical"]
        temporal_fail = [r for r in self.temporal_audit if r["status"] == "fail"]
        metric_fail = [r for r in self.metric_checks if r["status"] == "fail"]
        prediction_count = len(self.loaded.get("predictions", []))
        usable_folds = sum(1 for r in self.loaded.get("fold_plan", []) if as_bool(r.get("usable")))

        self.gate("critical_files_present",True,not missing_required,"critical",f"missing={len(missing_required)}","Run missing upstream phases.")
        self.gate("schema_contracts_complete",True,not critical_schema,"critical",f"critical_schema_issues={len(critical_schema)}","Align producer and consumer CSV contracts.")
        self.gate("primary_keys_unique",True,duplicates==0,"critical",f"duplicates={duplicates}","Fix ID generation or repeated append behavior.")
        self.gate("cross_phase_lineage",True,not lineage_fail,"critical",f"failed_relations={len(lineage_fail)}","Regenerate all downstream artifacts from a single coherent upstream run.")
        self.gate("semantic_invariants",True,not semantic_critical,"critical",f"critical_semantic_issues={len(semantic_critical)}","Repair direction/side, role, risk, or label semantics.")
        self.gate("walk_forward_temporal_boundaries",True,not temporal_fail,"critical",f"failed_folds={len(temporal_fail)}","Repair train/embargo/test boundary generation.")
        self.gate("writer_metric_reconciliation",True,not metric_fail,"error",f"failed_metrics={len(metric_fail)}","Re-run writer phases and reconcile summaries.")
        self.gate("oos_predictions_available",True,prediction_count>0,"error",f"predictions={prediction_count}","Generate usable Phase11 folds and OOS predictions.")
        self.gate("multiple_usable_folds",False,usable_folds>=3,"warning",f"usable_folds={usable_folds}","Collect enough history for at least three usable folds.")

    def readiness(self) -> str:
        blocking = [g for g in self.gates if g["required"] and not g["passed"] and g["severity"] == "critical"]
        failures = [g for g in self.gates if not g["passed"]]
        if blocking: return "BLOCKED_FOR_PHASE13"
        if failures: return "READY_WITH_WARNINGS"
        return "READY_FOR_PHASE13"

    def run(self) -> Dict[str, object]:
        self.load_and_audit_files()
        self.audit_lineage()
        self.audit_semantics()
        self.audit_temporal()
        self.audit_metrics()
        self.build_gates()
        return self.write_outputs()

    def write_outputs(self) -> Dict[str, object]:
        out = self.cfg.out_dir
        out.mkdir(parents=True, exist_ok=True)
        write_csv(out / "phase12_5_file_audit.csv", self.file_audit)
        write_csv(out / "phase12_5_schema_issues.csv", self.schema_issues)
        write_csv(out / "phase12_5_duplicate_report.csv", self.duplicate_report)
        write_csv(out / "phase12_5_lineage_reconciliation.csv", self.lineage)
        write_csv(out / "phase12_5_semantic_issues.csv", self.semantic_issues)
        write_csv(out / "phase12_5_temporal_audit.csv", self.temporal_audit)
        write_csv(out / "phase12_5_metric_reconciliation.csv", self.metric_checks)
        write_csv(out / "phase12_5_readiness_gates.csv", self.gates)

        status = self.readiness()
        summary = {
            "phase": "12.5", "readiness_status": status,
            "files_audited": len(self.file_audit),
            "schema_issue_count": len(self.schema_issues),
            "duplicate_issue_groups": len(self.duplicate_report),
            "lineage_checks": len(self.lineage),
            "lineage_failures": sum(1 for r in self.lineage if r["status"] == "fail"),
            "semantic_issue_count": len(self.semantic_issues),
            "critical_semantic_issue_count": sum(1 for r in self.semantic_issues if r["severity"] == "critical"),
            "temporal_failures": sum(1 for r in self.temporal_audit if r["status"] == "fail"),
            "metric_failures": sum(1 for r in self.metric_checks if r["status"] == "fail"),
            "gate_failures": sum(1 for g in self.gates if not g["passed"]),
            "research_boundary": "No execution, no filtering, no strategy mutation.",
        }
        (out / "phase12_5_readiness_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        self.write_markdown(out / "phase12_5_integrity_summary.md", summary)
        self.write_html(out / "phase12_5_integrity_report.html", summary)
        return summary

    def write_markdown(self, path: Path, summary: Mapping[str, object]) -> None:
        failed = [g for g in self.gates if not g["passed"]]
        lines = ["# EXP0017 Phase 12.5 — Pipeline Integrity Summary", "",
                 f"**Readiness:** `{summary['readiness_status']}`", "",
                 "Boundary: research integrity only. No execution, filtering, or strategy mutation.", "",
                 "## Counts"]
        for k,v in summary.items():
            if k not in {"phase","readiness_status","research_boundary"}: lines.append(f"- **{k}:** {v}")
        lines += ["", "## Failed gates"]
        if not failed: lines.append("- None.")
        for g in failed: lines.append(f"- `{g['gate_name']}` — {g['evidence']} — remediation: {g['remediation']}")
        path.write_text("\n".join(lines)+"\n", encoding="utf-8")

    def write_html(self, path: Path, summary: Mapping[str, object]) -> None:
        def table(rows: Sequence[Mapping[str, object]], limit: int = 200) -> str:
            if not rows: return "<p>No rows.</p>"
            headers = list(rows[0].keys())
            chunks = ["<table><thead><tr>"+"".join(f"<th>{html.escape(str(h))}</th>" for h in headers)+"</tr></thead><tbody>"]
            for row in rows[:limit]:
                chunks.append("<tr>"+"".join(f"<td>{html.escape(str(row.get(h,'')))}</td>" for h in headers)+"</tr>")
            chunks.append("</tbody></table>")
            return "\n".join(chunks)
        status = html.escape(str(summary["readiness_status"]))
        doc = f"""<!doctype html><html><head><meta charset='utf-8'><title>EXP0017 Phase 12.5 Integrity</title>
<style>body{{font-family:Arial,sans-serif;background:#101216;color:#e8e8e8;margin:24px}}table{{border-collapse:collapse;width:100%;font-size:12px;margin-bottom:30px}}th,td{{border:1px solid #3a3f48;padding:6px;vertical-align:top}}th{{background:#20242b}}tr:nth-child(even){{background:#171a20}}.status{{font-size:22px;font-weight:bold}}</style></head><body>
<h1>EXP0017 Phase 12.5 — Pipeline Integrity</h1><p class='status'>{status}</p><p>Research integrity only; no execution or strategy mutation.</p>
<h2>Readiness Gates</h2>{table(self.gates)}
<h2>File Audit</h2>{table(self.file_audit)}
<h2>Schema Issues</h2>{table(self.schema_issues)}
<h2>Lineage</h2>{table(self.lineage)}
<h2>Semantic Issues</h2>{table(self.semantic_issues)}
<h2>Temporal Audit</h2>{table(self.temporal_audit)}
<h2>Metric Reconciliation</h2>{table(self.metric_checks)}
</body></html>"""
        path.write_text(doc, encoding="utf-8")


def default_filenames() -> Dict[str, str]:
    return {
        "p07":"EXP0017_Phase07_Outcome_Study.csv",
        "p08_overall":"EXP0017_Phase08_Overall.csv",
        "p08_cgdr":"EXP0017_Phase08_By_CG_Direction_Role.csv",
        "p09_rank":"EXP0017_Phase09_Rankings_All.csv",
        "p09_short":"EXP0017_Phase09_Shortlist.csv",
        "p10":"EXP0017_Phase10_Model_Dataset.csv",
        "p10_summary":"EXP0017_Phase10_Label_Summary.csv",
        "p11_fold":"EXP0017_Phase11_Fold_Plan.csv",
        "p11_pred":"EXP0017_Phase11_Predictions.csv",
        "p11_metrics":"EXP0017_Phase11_Fold_Metrics.csv",
        "p11_bucket":"EXP0017_Phase11_Bucket_Validation.csv",
        "p11_summary":"EXP0017_Phase11_Experiment_Summary.csv",
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="EXP0017 Phase 12.5 pipeline integrity auditor")
    p.add_argument("--data-dir", default=".")
    p.add_argument("--out-dir", default="research/exp0017_phase12_5/outputs")
    p.add_argument("--max-rows", type=int, default=500_000)
    p.add_argument("--exact-lineage-min-pct", type=float, default=99.90)
    p.add_argument("--count-tolerance", type=int, default=0)
    p.add_argument("--fail-on-warning", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cfg = Config(Path(args.data_dir), Path(args.out_dir), args.max_rows,
                 args.exact_lineage_min_pct, args.count_tolerance,
                 args.fail_on_warning, default_filenames())
    summary = IntegrityAuditor(cfg).run()
    print(f"EXP0017 Phase12.5 complete: {summary['readiness_status']}")
    print(f"outputs: {cfg.out_dir}")
    if summary["readiness_status"] == "BLOCKED_FOR_PHASE13": return 2
    if summary["readiness_status"] == "READY_WITH_WARNINGS" and cfg.fail_on_warning: return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
