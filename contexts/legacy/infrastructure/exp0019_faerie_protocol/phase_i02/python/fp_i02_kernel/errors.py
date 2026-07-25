from __future__ import annotations

from typing import Any, Mapping


class FPI02Error(ValueError):
    """Closed, reason-code-bearing failure for the FP-I02 contract kernel."""

    def __init__(self, code: str, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.details = dict(details or {})
