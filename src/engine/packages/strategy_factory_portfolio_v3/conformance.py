from __future__ import annotations
from .golden import *
from .queue import rank_batch
from .capacity import estimate_capacity
from .allocator import allocate
from .stress import run_stress
from .validation import validate_portfolio
from .runtime import compile_runtime_bundle

def run_conformance():
    b=golden_batch();m=golden_model();l=golden_limits();r=rank_batch(b);q={x.candidate.candidate_id:estimate_capacity(x.candidate,b.as_of_ms) for x in r};p,ledger=allocate(b,m,l,q);s=run_stress(p,golden_stress(),l);v=validate_portfolio(p,s,{x.context_id:x.adjusted_score for x in p.selected});bundle=compile_runtime_bundle(p,l,m,v,ledger)
    return {'status':'pass','selected':len(p.selected),'contexts':p.context_count,'plan_hash':p.plan_hash,'bundle_hash':bundle.bundle_hash}
