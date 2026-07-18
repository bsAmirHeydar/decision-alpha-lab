from __future__ import annotations
from typing import Any
from .canonical import with_digest
from .errors import PolicyError
from .policies import GATE_IDS
from .schema_validation import validate_instance

HARD_FAIL_GATES={'INPUT_INTEGRITY','DATA_QUALITY_AND_LEAKAGE','DIAGNOSTIC_ISOLATION'}
REQUIRED_FOR_ELIGIBILITY=set(GATE_IDS)

def registry_snapshot()->dict[str,Any]:
    entries=[]
    for order,g in enumerate(GATE_IDS,1):
        entries.append({'gate_id':g,'order':order,'hard_fail':g in HARD_FAIL_GATES,'required_for_eligibility':True,'closed_world':True})
    return with_digest({'schema_version':'1.0.0','registry_id':'ACL07_GATE_REGISTRY_V1','closed_world':True,'entries':entries},'registry_digest')
def validate_registry(doc:dict[str,Any])->dict[str,Any]:
    validate_instance('gate_registry',doc)
    if doc!=registry_snapshot(): raise PolicyError('gate registry differs from closed-world reference')
    return doc
