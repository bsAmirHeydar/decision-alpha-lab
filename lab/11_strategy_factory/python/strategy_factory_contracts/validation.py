from __future__ import annotations
import math
import re

_SAFE_ID = re.compile(r"^[A-Za-z0-9_.:/-]+$")

class ContractValidationError(ValueError):
    pass

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractValidationError(message)

def validate_safe_identifier(value: str, field: str, max_length: int = 128, allow_empty: bool = False) -> None:
    if allow_empty and value == "":
        return
    require(isinstance(value, str), f"{field} must be a string")
    require(0 < len(value) <= max_length, f"{field} length out of range")
    require(value.isascii(), f"{field} must be ASCII")
    require(_SAFE_ID.fullmatch(value) is not None, f"{field} contains unsafe characters")

def validate_terminal_symbol(value: str, field: str = "symbol", max_length: int = 64, allow_empty: bool = False) -> None:
    """Validate a terminal symbol without applying internal identifier grammar.

    Broker symbols commonly contain prefixes and suffixes such as ``#US30``,
    ``EURUSD.a`` or ``XAUUSD-pro``. Wire delimiters and control/space
    characters remain forbidden.
    """
    if allow_empty and value == "":
        return
    require(isinstance(value, str), f"{field} must be a string")
    require(0 < len(value) <= max_length, f"{field} length out of range")
    require(value.isascii(), f"{field} must be ASCII")
    forbidden = {'|', ',', ';', '"', '\\'}
    require(all(ord(ch) > 32 and ch not in forbidden for ch in value),
            f"{field} contains unsafe characters")

def validate_finite(value: float, field: str) -> None:
    require(math.isfinite(value), f"{field} must be finite")
