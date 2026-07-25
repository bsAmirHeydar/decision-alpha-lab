from __future__ import annotations
from .models import build_model
from .contracts import CandidateSpec
from .numerics import max_abs_diff

def run_vectors(vectors):
    rows=[]
    for v in vectors:
        spec=CandidateSpec.from_mapping(v['candidate']);model=build_model(spec,int(v['input_dim']));outs,_=model.batch(v['inputs'],v.get('dts'))
        expected=v.get('expected_last')
        if expected is None:passed=all(all(abs(x)<1e9 for x in row) for row in outs);diff=0.0
        else:diff=max_abs_diff(outs[-1],expected);passed=diff<=float(v.get('tolerance',1e-10))
        rows.append({'vector_id':v['vector_id'],'candidate_id':spec.candidate_id,'passed':passed,'max_abs_diff':diff,'last_output':list(outs[-1])})
    return {'phase':'SAED_V4_12','rows':rows,'passed':all(r['passed'] for r in rows),'vector_count':len(rows)}
