from __future__ import annotations
from itertools import combinations
from .canonical import stable_id,content_hash
from .errors import BudgetError

def bounded_program_synthesis(rows,predicate_ids,target_treatment,max_terms=3,max_candidates=128):
    candidates=[]
    for k in range(1,min(max_terms,len(predicate_ids))+1):
        for combo in combinations(sorted(predicate_ids),k):
            if len(candidates)>=max_candidates:break
            tp=fp=fn=tn=0
            for r in rows:
                pred=all(bool(r['predicate_values'].get(p,False)) for p in combo);actual=r['target_treatment']==target_treatment
                tp+=pred and actual;fp+=pred and not actual;fn+=(not pred) and actual;tn+=(not pred) and (not actual)
            precision=tp/(tp+fp) if tp+fp else 0.0;recall=tp/(tp+fn) if tp+fn else 0.0
            fidelity=(tp+tn)/max(1,tp+tn+fp+fn);complexity=len(combo);score=fidelity-0.02*complexity
            candidates.append({'candidate_id':stable_id('program',{'c':combo,'t':target_treatment}),'conditions':list(combo),'target_treatment':target_treatment,'precision':precision,'recall':recall,'fidelity':fidelity,'complexity':complexity,'mdl_score':score})
    candidates.sort(key=lambda x:(-x['mdl_score'],x['complexity'],x['candidate_id']))
    return {'candidates':candidates,'champion':candidates[0] if candidates else None,'candidate_count':len(candidates),'search_hash':content_hash(candidates)}
