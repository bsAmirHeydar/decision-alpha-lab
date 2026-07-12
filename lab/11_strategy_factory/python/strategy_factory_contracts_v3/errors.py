"""Typed, machine-actionable failures for contract processing."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class ContractError(Exception):
    code: str
    message: str
    context: Mapping[str, Any] | None = None

    def __str__(self) -> str:
        suffix = "" if not self.context else f" context={dict(self.context)!r}"
        return f"{self.code}: {self.message}{suffix}"

class CanonicalizationError(ContractError): pass
class IdentityError(ContractError): pass
class KnownTimeError(ContractError): pass
class SchemaError(ContractError): pass
class MigrationError(ContractError): pass
class CompatibilityError(ContractError): pass
