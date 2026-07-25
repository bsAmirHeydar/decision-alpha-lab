"""Canonical JSON and fixed-scale numeric normalization.

The serializer is intentionally smaller than a general JSON encoder. It accepts
only contract-safe values and rejects raw binary floating point. Decimal values
must declare an explicit fixed scale, eliminating language-specific float text.
"""
from __future__ import annotations
from dataclasses import dataclass, fields, is_dataclass
from decimal import Decimal, ROUND_HALF_EVEN, InvalidOperation
from enum import Enum
from typing import Any, Mapping, Sequence
import json
from .errors import CanonicalizationError

@dataclass(frozen=True, slots=True)
class CanonicalDecimal:
    value: Decimal | str | int
    scale: int

    def normalized_text(self) -> str:
        if not isinstance(self.scale, int) or self.scale < 0 or self.scale > 18:
            raise CanonicalizationError("invalid_decimal_scale", "scale must be an integer from 0 through 18", {"scale": self.scale})
        try:
            decimal_value = Decimal(str(self.value))
            quantum = Decimal(1).scaleb(-self.scale)
            normalized = decimal_value.quantize(quantum, rounding=ROUND_HALF_EVEN)
        except (InvalidOperation, ValueError) as exc:
            raise CanonicalizationError("invalid_decimal", "decimal value cannot be normalized", {"value": str(self.value)}) from exc
        if not normalized.is_finite():
            raise CanonicalizationError("non_finite_decimal", "NaN and infinities are forbidden")
        if normalized == 0:
            normalized = abs(normalized)
        return format(normalized, f".{self.scale}f")

@dataclass(frozen=True, slots=True)
class CanonicalScaledInteger:
    units: int
    scale: int

    def normalized_text(self) -> str:
        if not isinstance(self.units, int) or isinstance(self.units, bool):
            raise CanonicalizationError("invalid_scaled_integer", "units must be an integer")
        return CanonicalDecimal(Decimal(self.units).scaleb(-self.scale), self.scale).normalized_text()


def _json_string(value: str) -> str:
    # ensure_ascii=True gives byte-stable U+XXXX escaping across Python and MQL5.
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))


def _normalize_dataclass(value: Any) -> dict[str, Any]:
    return {field.name: getattr(value, field.name) for field in fields(value)}


def canonical_json(value: Any) -> str:
    """Serialize a restricted value graph into canonical compact JSON."""
    if value is None: return "null"
    if value is True: return "true"
    if value is False: return "false"
    if isinstance(value, str): return _json_string(value)
    if isinstance(value, int) and not isinstance(value, bool): return str(value)
    if isinstance(value, (CanonicalDecimal, CanonicalScaledInteger)):
        return value.normalized_text()
    if isinstance(value, float):
        raise CanonicalizationError("raw_float_forbidden", "raw float values require an explicit CanonicalDecimal or CanonicalScaledInteger")
    if isinstance(value, Enum): return canonical_json(value.value)
    if is_dataclass(value): return canonical_json(_normalize_dataclass(value))
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise CanonicalizationError("non_string_key", "canonical objects require string keys")
        # Unicode codepoint order equals UTF-8 byte order for valid Unicode scalar sequences.
        parts=[_json_string(key)+":"+canonical_json(value[key]) for key in sorted(value)]
        return "{"+",".join(parts)+"}"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return "["+",".join(canonical_json(item) for item in value)+"]"
    raise CanonicalizationError("unsupported_type", "value is outside the canonical contract type system", {"type": type(value).__name__})


def canonical_utf8(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8", errors="strict")
