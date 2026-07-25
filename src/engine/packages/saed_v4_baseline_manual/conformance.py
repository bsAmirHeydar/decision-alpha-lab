from __future__ import annotations
from copy import deepcopy
from .compiler import compile_program
from .errors import BaselineManualError

def run_vectors(vectors:dict,view_package:dict,lattice:dict)->dict:
    results=[]
    for v in vectors['vectors']:
        source=deepcopy(v['program_source'])
        if v.get('mutation'):
            path=v['mutation']['path'].split('.')
            target=source
            for key in path[:-1]: target=target[int(key)] if isinstance(target,list) else target[key]
            key=path[-1]; target[int(key) if isinstance(target,list) else key]=v['mutation']['value']
        accepted=True; error=None
        try: compile_program(source,view_package,lattice)
        except BaselineManualError as exc: accepted=False; error=type(exc).__name__
        results.append({"vector_id":v['vector_id'],"expected_accept":v['expected_accept'],"actual_accept":accepted,"passed":accepted==v['expected_accept'],"error_class":error})
    return {"phase":"SAED_V4_10","results":results,"passed":all(x['passed'] for x in results),"vector_count":len(results)}
