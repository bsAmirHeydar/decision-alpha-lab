from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id
from .references import component_value, comparable
from .errors import ConstraintError

SUPPORTED={'eq','ne','ge','gt','le','lt','exists'}

def _compare(left:Any,operator:str,right:Any)->bool:
    if operator not in SUPPORTED: raise ConstraintError(f'unsupported operator: {operator}')
    if operator=='exists': return left is not None
    a,b=comparable(left),comparable(right)
    try:
        return {'eq':a==b,'ne':a!=b,'ge':a>=b,'gt':a>b,'le':a<=b,'lt':a<b}[operator]
    except TypeError as e: raise ConstraintError(f'incomparable values: {a!r}, {b!r}') from e

def evaluate_constraint(constraint:dict[str,Any],components:list[dict[str,Any]],capabilities:set[str])->dict[str,Any]:
    kind=constraint['kind']; op=constraint['operator']; left_ref=constraint['left_ref']
    if kind=='feature_predicate':
        status='deferred_known_time'; observed=None; expected=constraint.get('right_value'); reason='FEATURE_PREDICATE_DEFERRED_TO_V4_08_PATH_EVALUATION'
    elif kind=='capability_required':
        cap=left_ref.split(':',1)[1] if ':' in left_ref else ''
        ok=cap in capabilities; status='satisfied' if ok else 'violated'; observed=cap if ok else None; expected=cap; reason='CAPABILITY_PRESENT' if ok else 'CAPABILITY_MISSING'
    elif kind in ('parameter_relation','state_transition_guard'):
        left=component_value(components,left_ref)
        right=component_value(components,constraint['right_ref']) if constraint.get('right_ref') else constraint.get('right_value')
        ok=_compare(left,op,right);status='satisfied' if ok else 'violated';observed=left;expected=right;reason='CONSTRAINT_SATISFIED' if ok else 'CONSTRAINT_VIOLATED'
    else: raise ConstraintError(f'unsupported constraint kind: {kind}')
    seed={'constraint_name':constraint['constraint_name'],'status':status,'observed_value':observed,'expected_value':expected,'operator':op,'reason_code':reason}
    return {'evaluation_id':stable_id('ceval',seed),'evaluation_hash':content_hash(seed),**seed}

def evaluate_program(program:dict[str,Any],components:list[dict[str,Any]],capabilities:set[str],permit_deferred:bool)->tuple[list[dict[str,Any]],bool]:
    evaluations=[evaluate_constraint(c,components,capabilities) for c in sorted(program.get('constraints',[]),key=lambda c:c['constraint_name'])]
    if not permit_deferred and any(e['status']=='deferred_known_time' for e in evaluations): return evaluations,False
    return evaluations,not any(e['status']=='violated' for e in evaluations)
