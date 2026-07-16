from __future__ import annotations
from .canonical import stable_id,content_hash

def search(rule,rows,max_counterexamples=64):
    out=[]
    for r in rows:
        predicted=all(bool(r['predicate_values'].get(p,False)) for p in rule['conditions'])
        actual=r['target_treatment']==rule['target_treatment']
        if predicted!=actual:
            out.append({'counterexample_id':stable_id('cex',{'row':r['row_id'],'rule':rule['candidate_id']}),'row_id':r['row_id'],'predicted':predicted,'actual':actual,'violated_rule_id':rule['candidate_id'],'predicate_values':r['predicate_values']})
        if len(out)>=max_counterexamples:break
    return {'counterexamples':out,'count':len(out),'directive':'refine' if out else 'accept_synthetic_reference','report_hash':content_hash(out)}
def mutate_rows(rows,predicate_ids):
    out=[]
    for r in rows[:min(20,len(rows))]:
        for p in predicate_ids[:min(5,len(predicate_ids))]:
            m={**r,'row_id':r['row_id']+'__mut_'+p,'predicate_values':dict(r['predicate_values'])};m['predicate_values'][p]=not bool(m['predicate_values'].get(p,False));out.append(m)
    return out
