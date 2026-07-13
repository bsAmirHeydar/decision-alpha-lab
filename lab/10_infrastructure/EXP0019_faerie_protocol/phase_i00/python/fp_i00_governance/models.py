"""Closed evidence models for FP-I00."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Mapping

from .canonical import canonical_sha256


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class Health(str, Enum):
    READY = "READY"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    severity: Severity
    message: str
    path: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.code or not self.message:
            raise ValueError("issue code and message are required")


@dataclass(frozen=True, slots=True)
class ValidationReport:
    phase_id: str
    policy_version: str
    issues: tuple[ValidationIssue, ...]
    checks_run: int
    evidence_hash: str

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.ERROR)

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity is Severity.WARNING)

    @property
    def health(self) -> Health:
        if self.errors:
            return Health.BLOCKED
        if self.warnings:
            return Health.DEGRADED
        return Health.READY

    @property
    def passed(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "policy_version": self.policy_version,
            "health": self.health.value,
            "passed": self.passed,
            "checks_run": self.checks_run,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "issues": [
                {
                    "code": issue.code,
                    "severity": issue.severity.value,
                    "message": issue.message,
                    "path": issue.path,
                    "details": dict(issue.details),
                }
                for issue in self.issues
            ],
            "evidence_hash": self.evidence_hash,
        }


@dataclass(frozen=True, slots=True)
class SourceControlSnapshot:
    mode: str
    git_available: bool
    branch: str
    head_commit: str
    clean: bool | None
    phase_clean: bool | None
    changed_paths: tuple[str, ...]
    ignored_phase_changed_paths: tuple[str, ...]
    unrelated_changed_paths: tuple[str, ...]
    remote_urls: tuple[str, ...]

    @property
    def snapshot_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class DependencyRecord:
    dependency_id: str
    semantic_owner: str
    reuse_classification: str
    relative_root: str
    file_count: int
    aggregate_sha256: str
    exact_version: str
    required_for_phase: str
    mutation_allowed: bool


@dataclass(frozen=True, slots=True)
class TestRecord:
    context_id: str
    test_id: str
    test_type: str
    relative_path: str
    exists: bool
    compile_required: bool
    execution_command: str


@dataclass(frozen=True, slots=True)
class OwnershipRecord:
    path_prefix: str
    owner_phase: str
    ownership_class: str
    mutation_policy: str
    rollback_policy: str
