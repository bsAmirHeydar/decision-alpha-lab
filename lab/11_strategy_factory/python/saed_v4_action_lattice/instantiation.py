from __future__ import annotations
import copy
from typing import Any
from .canonical import content_hash
from .references import parse_component_ref

def instantiate_program(program:dict[str,Any], assignments:dict[str,Any])->list[dict[str,Any]]:
    components=copy.deepcopy(program['components'])
    by_slot={c['slot']:c for c in components}
    for ref,value in sorted(assignments.items()):
        slot,param=parse_component_ref(ref)
        by_slot[slot]['parameters'][param]=value
    for c in components:
        seed={k:v for k,v in c.items() if k!='component_hash'}
        c['component_hash']=content_hash(seed)
    return sorted(components,key=lambda c:(c['slot'],c['primitive_key']))
