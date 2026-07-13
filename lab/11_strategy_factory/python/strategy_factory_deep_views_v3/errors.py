"""Domain errors for UCE-I10 deep-view contracts.

The engine uses stable error codes because downstream orchestration, evidence
packaging, and MQL5 diagnostics must not parse free-form exception text.
"""

from __future__ import annotations

from typing import Any, Mapping


class DeepViewError(ValueError):
    """Fail-closed validation or execution error with a stable code."""

    def __init__(
        self,
        code: str,
        message: str,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.details = dict(details or {})

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": str(self),
            "details": self.details,
        }
