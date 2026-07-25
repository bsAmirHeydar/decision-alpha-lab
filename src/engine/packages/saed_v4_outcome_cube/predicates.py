from __future__ import annotations
from typing import Any
from .errors import ContractError

def evaluate(operator:str,observed:Any,expected:Any)->bool:
    if operator=='eq': return observed==expected
    if operator=='ne': return observed!=expected
    if operator=='gt': return float(observed)>float(expected)
    if operator=='ge': return float(observed)>=float(expected)
    if operator=='lt': return float(observed)<float(expected)
    if operator=='le': return float(observed)<=float(expected)
    if operator=='in': return observed in expected
    if operator=='exists': return observed is not None
    raise ContractError(f'unsupported predicate operator: {operator}')
