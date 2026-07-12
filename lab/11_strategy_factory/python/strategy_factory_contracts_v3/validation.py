"""Reusable fail-closed validators."""
from __future__ import annotations
import re
from collections.abc import Iterable
from .errors import ContractError

_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,127}$")
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def require(condition: bool, code: str, message: str, **context: object) -> None:
    if not condition:
        raise ContractError(code, message, context or None)


def require_safe_identifier(value: str, field: str, *, max_length: int = 128) -> str:
    if not isinstance(value, str) or not value or len(value) > max_length or not _SAFE_IDENTIFIER.fullmatch(value):
        raise ContractError("invalid_identifier", f"{field} is not a safe identifier", {"field": field, "value": value})
    return value


def require_sha256(value: str, field: str) -> str:
    if not isinstance(value, str) or not _HEX_64.fullmatch(value):
        raise ContractError("invalid_sha256", f"{field} must be lowercase 64-character SHA-256", {"field": field})
    return value


def require_unique(values: Iterable[str], field: str) -> tuple[str, ...]:
    materialized=tuple(values)
    if len(materialized) != len(set(materialized)):
        raise ContractError("duplicate_value", f"{field} contains duplicates", {"field": field})
    return materialized
