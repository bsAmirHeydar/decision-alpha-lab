"""Shared strict validation helpers."""
from __future__ import annotations
import re
from typing import Iterable, Any, Mapping, Sequence
from strategy_factory_contracts_v3 import CanonicalDecimal
from .errors import ContextSdkError
_SAFE=re.compile(r"^[A-Za-z0-9._:/-]{1,128}$")

def safe_id(value: str, field: str) -> str:
    if not isinstance(value,str) or not _SAFE.fullmatch(value):
        raise ContextSdkError("unsafe_identifier", f"{field} is not a safe identifier", {"field":field,"value":str(value)})
    return value

def nonempty_tuple(values: Iterable[str], field: str) -> tuple[str,...]:
    result=tuple(values)
    if not result: raise ContextSdkError("empty_collection", f"{field} may not be empty", {"field":field})
    for value in result: safe_id(value,field)
    if len(set(result)) != len(result): raise ContextSdkError("duplicate_value", f"{field} contains duplicates", {"field":field})
    return result

def sorted_unique(values: Iterable[str]) -> tuple[str,...]:
    return tuple(sorted(set(values)))


def contract_safe(value: Any, *, float_scale: int=8) -> Any:
    """Convert a value graph to the restricted canonical contract type system."""
    if isinstance(value,float): return CanonicalDecimal(str(value),float_scale)
    if isinstance(value,Mapping): return {str(k):contract_safe(v,float_scale=float_scale) for k,v in value.items()}
    if isinstance(value,Sequence) and not isinstance(value,(str,bytes,bytearray)):
        return [contract_safe(v,float_scale=float_scale) for v in value]
    return value
