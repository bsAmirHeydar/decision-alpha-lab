"""Reason-code-bearing failures for FP-I03."""
from __future__ import annotations
from typing import Any, Mapping


class FPI03Error(ValueError):
    def __init__(self, code: str, message: str, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.details = dict(details or {})
