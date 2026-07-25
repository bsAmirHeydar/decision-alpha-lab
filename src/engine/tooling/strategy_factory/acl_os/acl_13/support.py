from __future__ import annotations
from collections import Counter
from .canonical import with_digest
def build_support(slice_doc:dict)->dict:
    rows=slice_doc['rows']; occ=[r for r in rows if r['context_present']]
    states=Counter(r['state'] for r in occ); dirs=Counter(r['direction'] for r in occ)
    pos=sum(1 for r in occ if r['forward_delta']>0); neg=sum(1 for r in occ if r['forward_delta']<0); zero=len(occ)-pos-neg
    body={'schema_version':'1.0.0','total_observations':len(rows),'context_occurrences':len(occ),'non_occurrences':len(rows)-len(occ),'occurrence_rate':len(occ)/len(rows) if rows else 0,'positive_outcomes':pos,'negative_outcomes':neg,'zero_outcomes':zero,'state_support':dict(sorted(states.items())),'direction_support':dict(sorted(dirs.items())),'minimum_triage_support':12,'support_sufficient_for_triage':len(occ)>=12,'support_sufficient_for_validation':False,'validation_support_claimed':False}
    return with_digest(body,'support_diagnostics_digest')
