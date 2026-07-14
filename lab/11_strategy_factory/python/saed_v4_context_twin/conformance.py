from __future__ import annotations
from .compiler import compile_twin
from .errors import TwinError

def run_vectors(vectors):
    out=[]
    for v in vectors:
        try:
            m=compile_twin(v['context_spec'],v['seed']);actual='pass'
            detail=m.semantic_hash
        except Exception as e:
            actual='reject';detail=type(e).__name__+':'+str(e)
        out.append({'id':v['id'],'expected':v['expected'],'actual':actual,'passed':actual==v['expected'],'detail':detail})
    return out
