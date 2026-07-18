from __future__ import annotations
from itertools import combinations
from .canonical import with_digest,stable_id

def _jaccard(a:set[str],b:set[str])->int:
    return 10000 if not (a|b) else int(round(10000*len(a&b)/len(a|b)))
def detect(records:list[dict],threshold_bps:int,prior_fingerprints:dict[str,str]|None=None)->dict:
    prior_fingerprints=prior_fingerprints or {}
    groups={}
    for r in records: groups.setdefault(r['duplicate_fingerprint'],[]).append(r)
    clusters=[]; canonical=[]
    for fp,rows in sorted(groups.items()):
        rows=sorted(rows,key=lambda x:x['experience_id']); rep=rows[0]
        prior_entry=prior_fingerprints.get(fp)
        clusters.append(with_digest({'schema_version':'1.0.0','cluster_id':stable_id('DUPCL',fp),'duplicate_fingerprint':fp,'canonical_experience_id':rep['experience_id'],'member_experience_ids':[x['experience_id'] for x in rows],'member_count':len(rows),'prior_memory_entry_id':prior_entry,'exact_duplicate_count':len(rows)-1,'merge_semantics':'ALIAS_ONLY_NO_SOURCE_MUTATION'},'cluster_digest'))
        canonical.append(rep)
    near=[]
    eligible=[r for r in canonical if r['experience_class'] in {'INSUFFICIENT_EVIDENCE','NEGATIVE_VALIDATION','REPORTABLE_EVIDENCE'}]
    for a,b in combinations(sorted(eligible,key=lambda x:x['experience_id']),2):
        if a['duplicate_fingerprint']==b['duplicate_fingerprint']: continue
        q=_jaccard(set(a['bounded_research_questions']),set(b['bounded_research_questions']))
        u=_jaccard(set(a['unknown_gate_ids']),set(b['unknown_gate_ids']))
        score=(q+u)//2
        if score>=threshold_bps:
            near.append(with_digest({'schema_version':'1.0.0','pair_id':stable_id('NEARDUP',a['experience_id'],b['experience_id']),'left_experience_id':a['experience_id'],'right_experience_id':b['experience_id'],'question_jaccard_bps':q,'unknown_gate_jaccard_bps':u,'equivalence_score_bps':score,'auto_merge_allowed':False,'human_review_required':True},'pair_digest'))
    return with_digest({'schema_version':'1.0.0','record_count':len(records),'unique_fingerprint_count':len(groups),'exact_duplicate_count':sum(max(0,len(v)-1) for v in groups.values()),'clusters':clusters,'near_equivalence_count':len(near),'near_equivalences':near,'threshold_bps':threshold_bps,'source_records_mutated':False},'equivalence_report_digest')
