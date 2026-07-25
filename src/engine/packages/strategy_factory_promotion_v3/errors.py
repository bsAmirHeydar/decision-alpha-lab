"""Typed fail-closed errors for UCE-I12."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class PromotionError(ValueError):
    code: str
    message: str
    details: Mapping[str, Any] | None = None
    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
