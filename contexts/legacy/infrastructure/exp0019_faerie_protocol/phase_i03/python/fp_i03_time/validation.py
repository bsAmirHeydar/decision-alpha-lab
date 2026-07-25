"""High-level validation helpers for FP-I03 outputs."""
from __future__ import annotations
from dataclasses import dataclass
from fp_i02_kernel.canonical import canonical_sha256
from .contracts import CalendarSnapshot, TimeKernelConfig, canonical_registry_snapshot
from .enums import CalendarHealth, CalendarSegment


@dataclass(frozen=True, slots=True)
class ValidationFinding:
    code: str
    severity: str
    detail: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    findings: tuple[ValidationFinding, ...]
    passed: bool
    report_hash: str


def validate_snapshot(value: CalendarSnapshot, config: TimeKernelConfig | None = None) -> ValidationReport:
    config = config or TimeKernelConfig()
    findings: list[ValidationFinding] = []
    if value.config_hash != config.config_hash:
        findings.append(ValidationFinding("FP_TRC_CONFIG_HASH_MISMATCH", "ERROR", "snapshot config hash differs"))
    if value.segment in (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N):
        if value.session is None or not value.session.contains_reference_time:
            findings.append(ValidationFinding("FP_TRC_SESSION_OWNERSHIP_MISMATCH", "CRITICAL", "active session missing containment"))
    if value.week.contains_reference_time != (value.week.start_utc_ms <= value.reference_utc_ms < value.week.end_utc_ms):
        findings.append(ValidationFinding("FP_TRC_WEEK_CONTAINMENT_MISMATCH", "CRITICAL", "week containment flag differs"))
    if value.health is not CalendarHealth.READY:
        findings.append(ValidationFinding("FP_TRC_HEALTH_NOT_READY", "ERROR", value.health.value))
    passed = not any(item.severity in ("ERROR", "CRITICAL") for item in findings)
    material = {"snapshot_id": value.snapshot_id, "config_hash": config.config_hash, "findings": findings, "passed": passed}
    return ValidationReport(tuple(findings), passed, canonical_sha256(material))


def validate_registry() -> ValidationReport:
    registry = canonical_registry_snapshot()
    findings = [] if registry.frozen else [ValidationFinding("FP_TRC_SESSION_REGISTRY_MUTABLE", "CRITICAL", "registry not frozen")]
    material = {"registry_hash": registry.registry_hash, "findings": findings}
    return ValidationReport(tuple(findings), not findings, canonical_sha256(material))
