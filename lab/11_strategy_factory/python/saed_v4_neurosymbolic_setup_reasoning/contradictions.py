from __future__ import annotations
from .canonical import content_hash

def audit_facts(facts):
    slots={};rows=[]
    for f in facts:
        k=(f['subject_id'],f['concept_id'],repr(f['value']))
        slots.setdefault(k,set()).add(f['polarity'])
    for k,v in sorted(slots.items()):
        if len(v)>1:rows.append({'subject_id':k[0],'concept_id':k[1],'value_repr':k[2],'polarities':sorted(v)})
    return {'contradictions':rows,'count':len(rows),'directive':'quarantine' if rows else 'continue_reference','report_hash':content_hash(rows)}
def audit_decisions(decisions):
    by={}
    for d in decisions:by.setdefault(d['subject_id'],set()).add((d['effect'],d['treatment_id']))
    rows=[{'subject_id':s,'decision_pairs':sorted(list(v))} for s,v in sorted(by.items()) if len({d['treatment_id'] for d in decisions if d['subject_id']==s and d['effect']=='recommend' and d['manual_doctrine']})>1]
    return {'decision_contradictions':rows,'count':len(rows),'directive':'abstain' if rows else 'continue_reference','report_hash':content_hash(rows)}
