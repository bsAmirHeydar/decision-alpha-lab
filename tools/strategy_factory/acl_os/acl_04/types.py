from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class Lane(StrEnum):
    HUMAN = "HUMAN"
    AI = "AI"
    BASELINE = "BASELINE"

class CandidateStatus(StrEnum):
    COMPILED = "COMPILED"
    INVALID = "INVALID"
    DUPLICATE = "DUPLICATE"
    ELIGIBLE_FOR_BATCH_DEFINITION = "ELIGIBLE_FOR_BATCH_DEFINITION"
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"

class Severity(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"

@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: Severity
    path: str
    message: str
    remediation: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "path": self.path,
            "message": self.message,
            "remediation": self.remediation,
            "details": self.details,
        }
