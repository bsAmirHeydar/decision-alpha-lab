from __future__ import annotations
from copy import deepcopy
from .adapters import run_read_only_adapter
from .fixtures import fixtures
from .models import AdapterRunEvidence
from .enums import CompatibilityStatus

def run_fixture(fixture_id,pair):
    key,payload=pair; original=deepcopy(payload)
    output,before,after,out_hash,repeat_hash=run_read_only_adapter(key,payload)
    blockers=[]
    if before!=after or payload!=original:blockers.append('SOURCE_MUTATED')
    if out_hash!=repeat_hash:blockers.append('NON_DETERMINISTIC_OUTPUT')
    return AdapterRunEvidence(fixture_id,key,before,after,out_hash,repeat_hash,before==after and payload==original,out_hash==repeat_hash,CompatibilityStatus.PASS if not blockers else CompatibilityStatus.FAIL,tuple(blockers),())

def run_all_fixtures(): return tuple(run_fixture(k,v) for k,v in sorted(fixtures().items()))
