from __future__ import annotations
from statistics import mean
from .canonical import stable_id,with_digest
def _match(row:dict,clause:dict)->bool:
    field=clause['field']; op=clause['operator']; value=clause['value']; current=row.get(field)
    if op=='EQ': return current==value
    if op=='GTE': return current>=value
    if op=='LTE': return current<=value
    raise ValueError('ACL13_UNREGISTERED_OPERATOR')
def build_catalog(req:dict,slice_doc:dict)->dict:
    rows=slice_doc['rows']; families=[]
    for spec in req['declared_setup_families']:
        selected=[r for r in rows if all(_match(r,c) for c in spec['clauses'])]
        values=[r['forward_delta'] for r in selected]
        body={'schema_version':'1.0.0','family_id':spec['family_id'],'family_name':spec['family_name'],'clauses':spec['clauses'],'support':len(selected),'mean_forward_delta':mean(values) if values else 0.0,'hit_rate':sum(1 for v in values if v>0)/len(values) if values else 0.0,'minimum_support_met':len(selected)>=spec['minimum_support'],'source':'PREDECLARED_BOUNDED_FAMILY','dynamic_generation_used':False,'selection_authority':False}
        families.append(with_digest(body,'family_result_digest'))
    families.sort(key=lambda x:x['family_id'])
    return with_digest({'schema_version':'1.0.0','catalog_id':stable_id('SETUPCAT',req['assessment_request_id'],length=28),'family_count':len(families),'families':families,'dynamic_generation_used':False,'ai_generation_used':False,'promotion_allowed':False},'catalog_digest')
