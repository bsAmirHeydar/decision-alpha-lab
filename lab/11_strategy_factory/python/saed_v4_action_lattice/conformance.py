from __future__ import annotations
from .canonical import content_hash,stable_id

def run_vectors(vectors:list[dict],runner)->dict:
    rows=[]
    for v in vectors:
        try:
            runner(v);actual='accepted'
        except Exception as e:
            actual='rejected';error_type=type(e).__name__
        else:error_type=None
        passed=actual==v['expected_status'] and (v.get('expected_error_type') in (None,error_type))
        rows.append({'vector_id':v['vector_id'],'expected_status':v['expected_status'],'actual_status':actual,'actual_error_type':error_type,'passed':passed})
    seed={'rows':rows,'passed_count':sum(r['passed'] for r in rows),'failed_count':sum(not r['passed'] for r in rows)}
    return {'result_id':stable_id('latticeconf',seed),'result_hash':content_hash(seed),**seed}
