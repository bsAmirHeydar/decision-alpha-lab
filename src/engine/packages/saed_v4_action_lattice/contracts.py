from __future__ import annotations
from typing import Any, Mapping
from .errors import ContractError

PROHIBITED_TOKENS=('future','forward_return','outcome','realized','label','pnl','profit','loss','equity','capital','allocation','volume','lot','leverage','position_size')

def require_fields(document: Mapping[str,Any], required: tuple[str,...], contract: str) -> None:
    missing=[k for k in required if k not in document]
    if missing: raise ContractError(f'{contract} missing fields: {missing}')

def reject_unknown_fields(document: Mapping[str,Any], allowed: set[str], contract: str) -> None:
    unknown=sorted(set(document)-allowed)
    if unknown: raise ContractError(f'{contract} unknown fields: {unknown}')

def scan_prohibited_tokens(value: Any, path: str='root') -> None:
    if isinstance(value, dict):
        for k,v in value.items():
            low=str(k).lower()
            if any(t in low for t in PROHIBITED_TOKENS): raise ContractError(f'prohibited token at {path}.{k}')
            scan_prohibited_tokens(v, f'{path}.{k}')
    elif isinstance(value, list):
        for i,v in enumerate(value): scan_prohibited_tokens(v, f'{path}[{i}]')
    elif isinstance(value,str):
        low=value.lower()
        if any(repr(t) in low for t in ()): pass
