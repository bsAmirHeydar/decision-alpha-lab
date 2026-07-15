from __future__ import annotations
from decimal import Decimal, InvalidOperation
from typing import Any
from .errors import ConstraintError

def parse_component_ref(ref: str) -> tuple[str,str]:
    if not ref.startswith('component:') or '.' not in ref:
        raise ConstraintError(f'invalid component reference: {ref}')
    slot_param=ref[len('component:'):]
    slot,param=slot_param.split('.',1)
    if not slot or not param: raise ConstraintError(f'invalid component reference: {ref}')
    return slot,param

def component_value(components: list[dict[str,Any]], ref: str) -> Any:
    slot,param=parse_component_ref(ref)
    matches=[c for c in components if c['slot']==slot]
    if len(matches)!=1: raise ConstraintError(f'component slot not unique: {slot}')
    if param not in matches[0]['parameters']: raise ConstraintError(f'unknown parameter reference: {ref}')
    return matches[0]['parameters'][param]

def comparable(value: Any) -> Any:
    if isinstance(value,(int,float,Decimal)): return Decimal(str(value))
    if isinstance(value,str):
        try: return Decimal(value)
        except InvalidOperation: return value
    return value
