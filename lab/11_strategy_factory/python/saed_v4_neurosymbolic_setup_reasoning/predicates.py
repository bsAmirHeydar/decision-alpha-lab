from __future__ import annotations
from .contracts import PredicateRegistry
from .errors import RuleError

def compile_predicates(mapping,ontology):
    p=PredicateRegistry.from_mapping(mapping);out={}
    for row in p.predicates:
        if row['concept_id'] not in ontology['concepts']:raise RuleError('predicate concept outside ontology')
        out[row['predicate_id']]=dict(row)
    return {'exact_version':p.exact_version,'predicates':out,'missing_value_policy':p.missing_value_policy,'future_fact_policy':p.future_fact_policy}
def compare(value,p):
    op=p['operator'];thr=p['threshold'];vals=p['values']
    if op=='exists':r=value is not None
    elif op=='not_missing':r=value is not None
    elif value is None:return None
    elif op=='eq':r=value==thr
    elif op=='neq':r=value!=thr
    elif op=='gt':r=float(value)>float(thr)
    elif op=='ge':r=float(value)>=float(thr)
    elif op=='lt':r=float(value)<float(thr)
    elif op=='le':r=float(value)<=float(thr)
    elif op=='between':r=float(vals[0])<=float(value)<=float(vals[1])
    elif op=='in':r=value in vals
    else:raise RuleError('unknown predicate operator')
    return not r if p.get('negated') else r
def evaluate_predicate(compiled,store,subject_id,predicate_id):
    if predicate_id not in compiled['predicates']:raise RuleError('unknown predicate')
    p=compiled['predicates'][predicate_id];facts=store.query(subject_id,p['concept_id'])
    if not facts:return None
    return any(compare(x['value'],p) is True and x['polarity']==1 for x in facts)
