from __future__ import annotations
from collections.abc import Mapping
from .contracts import Predicate
from .errors import PolicyError

def resolve_field(payload:Mapping,field:str):
    cur=payload
    for part in field.split('.'):
        if not isinstance(cur,Mapping) or part not in cur: return None,False
        cur=cur[part]
    return cur,True

def evaluate_predicate(predicate:Predicate,payload:Mapping)->bool:
    actual,exists=resolve_field(payload,predicate.field); op=predicate.operator; expected=predicate.value
    if op=='exists': return exists is bool(expected)
    if not exists:return False
    try:
        if op=='eq': return actual==expected
        if op=='ne': return actual!=expected
        if op=='gt': return actual>expected
        if op=='ge': return actual>=expected
        if op=='lt': return actual<expected
        if op=='le': return actual<=expected
        if op=='in': return actual in expected
        if op=='not_in': return actual not in expected
        if op=='between': return len(expected)==2 and expected[0]<=actual<=expected[1]
    except TypeError as exc: raise PolicyError('predicate_type_mismatch','predicate values are not comparable',{'field':predicate.field}) from exc
    raise PolicyError('unsupported_operator',f'unsupported operator {op}')
def all_match(predicates,payload): return all(evaluate_predicate(p,payload) for p in predicates)
def any_match(predicates,payload): return any(evaluate_predicate(p,payload) for p in predicates)
