from __future__ import annotations
from statistics import mean
from .canonical import with_digest
def build_value(slice_doc:dict,support:dict,baselines:dict,catalog:dict)->dict:
    occ=[r for r in slice_doc['rows'] if r['context_present']]
    def component(field:str)->dict:
        high=[r['forward_delta'] for r in occ if r[field]>=0.6]; low=[r['forward_delta'] for r in occ if r[field]<0.6]
        return {'component_id':field.upper(),'high_support':len(high),'low_support':len(low),'high_mean':mean(high) if high else 0.0,'low_mean':mean(low) if low else 0.0,'descriptive_spread':(mean(high) if high else 0.0)-(mean(low) if low else 0.0)}
    comps=[component('x_location_score'),component('y_state_score'),component('optionality_score')]
    best=max(catalog['families'],key=lambda x:(x['mean_forward_delta'],x['support'])) if catalog['families'] else None
    body={'schema_version':'1.0.0','context_occurrence_support':support['context_occurrences'],'conditioned_mean':baselines['conditioned_mean'],'always_participate_mean':baselines['always_participate_mean'],'random_mean':baselines['random_mean'],'conditioned_minus_random_mean':baselines['conditioned_minus_random_mean'],'components':comps,'best_declared_family_id':best['family_id'] if best else None,'best_declared_family_support':best['support'] if best else 0,'best_declared_family_mean':best['mean_forward_delta'] if best else 0.0,'value_signal_observed':support['support_sufficient_for_triage'] and baselines['conditioned_exceeds_random_p90'],'alpha_claimed':False,'causal_claimed':False,'validation_claimed':False}
    return with_digest(body,'value_decomposition_digest')
