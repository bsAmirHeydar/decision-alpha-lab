"""Data, causality, lineage, and execution audit functions."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AuditFinding:
    finding_id: str
    passed: bool
    severity: str
    message: str
    count: int = 0
    details: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class AuditReport:
    report_id: str
    passed: bool
    findings: Sequence[AuditFinding]

    def to_dict(self) -> Mapping[str, Any]:
        return {
            "report_id": self.report_id,
            "passed": self.passed,
            "findings": [asdict(item) for item in self.findings],
        }


def audit_bar_data(frame: pd.DataFrame) -> AuditReport:
    findings = []
    required = {"timestamp_utc", "symbol", "open", "high", "low", "close"}
    missing = required - set(frame.columns)
    findings.append(AuditFinding("BAR_SCHEMA", not missing, "hard", f"missing columns: {sorted(missing)}", len(missing)))
    if missing:
        return AuditReport("bar_data_audit", False, tuple(findings))
    work = frame.copy()
    work["timestamp_utc"] = pd.to_datetime(work["timestamp_utc"], utc=True, errors="coerce")
    bad_time = int(work["timestamp_utc"].isna().sum())
    findings.append(AuditFinding("BAR_TIMESTAMP_PARSE", bad_time == 0, "hard", "timestamps must parse as UTC", bad_time))
    duplicate = int(work.duplicated(["symbol", "timestamp_utc"]).sum())
    findings.append(AuditFinding("BAR_DUPLICATE", duplicate == 0, "hard", "duplicate symbol/timestamp rows", duplicate))
    invalid_ohlc = int(((work["high"] < work[["open", "close", "low"]].max(axis=1)) | (work["low"] > work[["open", "close", "high"]].min(axis=1))).sum())
    findings.append(AuditFinding("BAR_OHLC_GEOMETRY", invalid_ohlc == 0, "hard", "invalid OHLC geometry", invalid_ohlc))
    non_finite = int((~np.isfinite(work[["open", "high", "low", "close"]].astype(float))).sum().sum())
    findings.append(AuditFinding("BAR_FINITE", non_finite == 0, "hard", "non-finite prices", non_finite))
    spread_negative = 0
    if {"bid", "ask"}.issubset(work.columns):
        spread_negative = int((work["ask"] < work["bid"]).sum())
    findings.append(AuditFinding("BAR_SPREAD", spread_negative == 0, "hard", "ask below bid", spread_negative))
    return AuditReport("bar_data_audit", all(f.passed or f.severity != "hard" for f in findings), tuple(findings))


def audit_model_dataset(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str],
    outcome_columns: Sequence[str] = ("net_r", "mfe_r", "mae_r", "exit_reason"),
) -> AuditReport:
    findings = []
    required = {"event_id", "candidate_id", "known_time_utc", "snapshot_time_utc", "label_end_time_utc"}
    missing = required - set(frame.columns)
    findings.append(AuditFinding("DATASET_SCHEMA", not missing, "hard", f"missing columns: {sorted(missing)}", len(missing)))
    if missing:
        return AuditReport("model_dataset_audit", False, tuple(findings))
    work = frame.copy()
    for column in ("known_time_utc", "snapshot_time_utc", "label_end_time_utc"):
        work[column] = pd.to_datetime(work[column], utc=True, errors="coerce")
    duplicate = int(work["candidate_id"].duplicated().sum())
    findings.append(AuditFinding("CANDIDATE_UNIQUENESS", duplicate == 0, "hard", "duplicate candidate IDs", duplicate))
    snapshot_future = int((work["snapshot_time_utc"] < work["known_time_utc"]).sum())
    findings.append(AuditFinding("SNAPSHOT_AFTER_KNOWN", snapshot_future == 0, "hard", "snapshot precedes event known time", snapshot_future))
    label_invalid = int((work["label_end_time_utc"] < work["snapshot_time_utc"]).sum())
    findings.append(AuditFinding("LABEL_HORIZON", label_invalid == 0, "hard", "label ends before decision snapshot", label_invalid))
    leakage_names = [feature for feature in feature_columns if feature in outcome_columns or feature.startswith("label_") or feature.endswith("__outcome")]
    findings.append(AuditFinding("FEATURE_NAME_LEAKAGE", not leakage_names, "hard", f"outcome-like features: {leakage_names}", len(leakage_names)))
    missing_features = [feature for feature in feature_columns if feature not in work.columns]
    findings.append(AuditFinding("FEATURE_SCHEMA", not missing_features, "hard", f"missing features: {missing_features}", len(missing_features)))
    if "market_event_cluster_id" in work.columns:
        empty_cluster = int(work["market_event_cluster_id"].isna().sum())
        findings.append(AuditFinding("CLUSTER_ID", empty_cluster == 0, "warning", "rows without market-event cluster", empty_cluster))
    return AuditReport("model_dataset_audit", all(f.passed or f.severity != "hard" for f in findings), tuple(findings))


def audit_fold_separation(
    frame: pd.DataFrame,
    train_index: Sequence[int],
    test_index: Sequence[int],
    *,
    time_col: str = "known_time_utc",
    label_end_col: str = "label_end_time_utc",
    cluster_col: str = "market_event_cluster_id",
) -> AuditReport:
    train = frame.iloc[list(train_index)].copy()
    test = frame.iloc[list(test_index)].copy()
    findings = []
    overlap = set(train.index) & set(test.index)
    findings.append(AuditFinding("ROW_DISJOINT", not overlap, "hard", "train/test row overlap", len(overlap)))
    train[label_end_col] = pd.to_datetime(train[label_end_col], utc=True)
    test[time_col] = pd.to_datetime(test[time_col], utc=True)
    future_overlap = int((train[label_end_col] >= test[time_col].min()).sum())
    findings.append(AuditFinding("LABEL_PURGE", future_overlap == 0, "hard", "training labels overlap test start", future_overlap))
    if cluster_col in frame.columns:
        cluster_overlap = set(train[cluster_col].dropna()) & set(test[cluster_col].dropna())
        findings.append(AuditFinding("CLUSTER_DISJOINT", not cluster_overlap, "hard", "clusters cross train/test", len(cluster_overlap)))
    return AuditReport("fold_separation_audit", all(f.passed for f in findings), tuple(findings))
