from __future__ import annotations
from typing import Any
from .errors import ContractError,KnownTimeError

def _atom(atom_id:str,args:list[Any],row:dict[str,Any],lane:str)->bool:
    if atom_id=='ALWAYS_TRUE': return True
    if atom_id=='CONTEXT_STATE_IS':
        state='CONFIRMED' if float(row.get('feature_y',0))>=0 else 'INVALIDATED'; return state==args[0]
    if atom_id=='FEATURE_COMPARE':
        feature,op,value=args; actual=float(row.get('feature_y' if feature=='close_price' else feature,0)); value=float(value)
        return {'>=':actual>=value,'>':actual>value,'<=':actual<=value,'<':actual<value,'==':actual==value}.get(op,False)
    if atom_id=='ELAPSED_BARS_COMPARE': return False
    if atom_id=='MISSINGNESS_IS_CLEAR': return True
    if atom_id=='FRESHNESS_WITHIN': return True
    if atom_id=='MANUAL_CONFIRMATION_IS': return bool(args[0]) is False
    if atom_id=='FUTURE_OUTCOME_IS':
        if lane!='DIAGNOSTIC': raise KnownTimeError('future outcome atom outside diagnostic lane')
        return (row.get('primary_label')=='UP')==(args[0]=='POSITIVE')
    raise ContractError(f'unknown atom: {atom_id}')
def evaluate_expr(expr:dict[str,Any],row:dict[str,Any],lane:str)->bool:
    op=expr['op']
    if op=='ATOM': return _atom(expr['atom_id'],expr.get('args',[]),row,lane)
    if op=='ALL': return all(evaluate_expr(x,row,lane) for x in expr['children'])
    if op=='ANY': return any(evaluate_expr(x,row,lane) for x in expr['children'])
    if op=='NOT': return not evaluate_expr(expr['child'],row,lane)
    raise ContractError(f'unknown expression op: {op}')
def evaluate_policy(candidate:dict[str,Any],row:dict[str,Any],lane:str)->dict[str,Any]:
    clauses=candidate['policy_ir']['clauses']
    for kind in ('ABSTENTION','INVALIDATION'):
        for c in sorted((x for x in clauses if x['kind']==kind),key=lambda x:x['priority']):
            if evaluate_expr(c['when'],row,lane): return {'decision':c['action'],'direction':None,'clause_id':c['clause_id']}
    for c in sorted((x for x in clauses if x['kind']=='ENTRY'),key=lambda x:x['priority']):
        if evaluate_expr(c['when'],row,lane): return {'decision':c['action'],'direction':1 if c['action']=='ENTER_LONG' else -1,'clause_id':c['clause_id']}
    return {'decision':'NO_SIGNAL','direction':None,'clause_id':None}
