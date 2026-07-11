from __future__ import annotations
from dataclasses import dataclass
from .models import DatasetManifest, DatasetRow
from .hashing import stable_id

@dataclass(frozen=True, slots=True)
class DatasetLeakageFinding:
    code: str
    severity: str
    row_id: str
    message: str

    @property
    def finding_hash(self) -> str:
        return stable_id("dfind", f"{self.code}|{self.severity}|{self.row_id}|{self.message}")

@dataclass(frozen=True, slots=True)
class DatasetAuditReport:
    dataset_hash: str
    findings: tuple[DatasetLeakageFinding, ...]
    fatal_count: int
    warning_count: int
    audit_hash: str


def audit_dataset(manifest: DatasetManifest, rows: tuple[DatasetRow, ...], feature_count: int) -> DatasetAuditReport:
    findings: list[DatasetLeakageFinding] = []
    seen_rows: set[str] = set()
    cluster_roles: dict[tuple[str, str], int] = {}
    for row in rows:
        try:
            row.validate(feature_count)
        except ValueError as error:
            findings.append(DatasetLeakageFinding("ROW_CONTRACT", "FATAL", row.row_id, str(error)))
        if row.row_id in seen_rows:
            findings.append(DatasetLeakageFinding("DUPLICATE_ROW", "FATAL", row.row_id, "duplicate dataset-row identity"))
        seen_rows.add(row.row_id)
        key = (row.fold_id, row.cluster_id)
        prior = cluster_roles.get(key)
        if prior is not None and prior != int(row.role):
            findings.append(DatasetLeakageFinding("CLUSTER_ROLE_SPLIT", "FATAL", row.row_id, "cluster crosses roles inside one fold"))
        cluster_roles[key] = int(row.role)
        if row.known_time_utc_msc > row.decision_time_utc_msc:
            findings.append(DatasetLeakageFinding("FUTURE_FEATURE", "FATAL", row.row_id, "feature known time follows decision time"))
        if row.resolved_time_utc_msc < row.decision_time_utc_msc:
            findings.append(DatasetLeakageFinding("EARLY_LABEL", "FATAL", row.row_id, "label resolves before decision time"))
    if manifest.row_count != len(rows):
        findings.append(DatasetLeakageFinding("ROW_COUNT_MISMATCH", "FATAL", "", "manifest row count differs from row collection"))
    if not rows:
        findings.append(DatasetLeakageFinding("EMPTY_DATASET", "FATAL", "", "dataset has no rows"))
    findings = sorted(findings, key=lambda f: (f.severity, f.code, f.row_id, f.finding_hash))
    fatal_count = sum(f.severity == "FATAL" for f in findings)
    warning_count = sum(f.severity == "WARNING" for f in findings)
    payload = manifest.dataset_hash + "|" + "|".join(f.finding_hash for f in findings)
    return DatasetAuditReport(manifest.dataset_hash, tuple(findings), fatal_count, warning_count, stable_id("daudit", payload))


def assert_no_fatal_dataset_leakage(report: DatasetAuditReport) -> None:
    if report.fatal_count:
        raise ValueError(f"dataset leakage audit failed with {report.fatal_count} fatal findings")
