from __future__ import annotations
from .canonical import content_hash

def run_vectors(vectors):
    results=[]
    for v in vectors['vectors']:
        observed=content_hash(v['input']);results.append({'vector_id':v['vector_id'],'expected_hash':v['expected_hash'],'observed_hash':observed,'passed':observed==v['expected_hash']})
    return {'phase':'SAED_V4_08','vector_count':len(results),'passed_count':sum(r['passed'] for r in results),'all_passed':all(r['passed'] for r in results),'results':results}
