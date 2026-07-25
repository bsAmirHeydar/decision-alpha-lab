from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class MigrationAction(str, Enum):
    REUSE_AS_IS = "REUSE_AS_IS"
    ADAPT = "ADAPT"
    WRAP = "WRAP"
    MIGRATE = "MIGRATE"
    DEPRECATE = "DEPRECATE"
    DELETE_LATER = "DELETE_LATER"
    REVIEW = "REVIEW"


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class FileRecord:
    path: str
    extension: str
    size_bytes: int
    line_count: int | None
    sha256: str
    is_binary: bool
    is_empty: bool
    category: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleRecord:
    module_id: str
    path_prefix: str
    capability: str
    action: MigrationAction
    reason: str
    risk: Severity
    current_owner: str
    target_owner: str
    evidence: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["action"] = self.action.value
        data["risk"] = self.risk.value
        data["evidence"] = list(self.evidence)
        return data


@dataclass(frozen=True)
class AuthorityFinding:
    path: str
    line: int
    token: str
    authority_type: str
    severity: Severity
    snippet: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True)
class ContractRecord:
    path: str
    symbol: str
    kind: str
    public_methods: tuple[str, ...]
    imports: tuple[str, ...]
    notes: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["public_methods"] = list(self.public_methods)
        data["imports"] = list(self.imports)
        return data


@dataclass(frozen=True)
class DuplicateCapability:
    capability: str
    implementations: tuple[str, ...]
    overlap_basis: str
    migration_decision: str
    severity: Severity

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["implementations"] = list(self.implementations)
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True)
class MigrationRisk:
    risk_id: str
    title: str
    category: str
    likelihood: str
    impact: str
    severity: Severity
    evidence: tuple[str, ...]
    mitigation: str
    owner_phase: str
    status: str = "OPEN"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["evidence"] = list(self.evidence)
        return data


@dataclass
class AuditResult:
    repo_root: Path
    generated_at_utc: str
    git_commit: str
    files: list[FileRecord]
    modules: list[ModuleRecord]
    authority_findings: list[AuthorityFinding]
    contracts: list[ContractRecord]
    duplicates: list[DuplicateCapability]
    risks: list[MigrationRisk]
    test_baseline: dict[str, Any]
    summary: dict[str, Any]
