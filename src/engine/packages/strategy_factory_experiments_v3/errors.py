"""Typed failures for UCE-I11 experiment orchestration.

Every public failure carries a stable machine-readable code.  Callers must not
infer semantics from exception text because scheduler, ledger, and governance
surfaces consume the code directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ExperimentErrorPayload:
    code: str
    message: str
    details: Mapping[str, Any]


class ExperimentError(ValueError):
    def __init__(self, code: str, message: str, details: Mapping[str, Any] | None = None) -> None:
        self.payload = ExperimentErrorPayload(code, message, dict(details or {}))
        super().__init__(f"{code}: {message}")

    @property
    def code(self) -> str:
        return self.payload.code

    @property
    def details(self) -> Mapping[str, Any]:
        return self.payload.details
