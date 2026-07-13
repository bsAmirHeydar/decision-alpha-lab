from __future__ import annotations
from pathlib import Path
import csv,json
from .models import DependencyPin
from .enums import *

def load_json(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def load_dependency_pins(repo:Path):
    p=repo/'lab/10_infrastructure/EXP0019_faerie_protocol/phase_i01/config/FP_I01_COMPATIBILITY_POLICY.v1.json'
    policy=load_json(p);pins=[]
    for d in policy['dependencies']:
        pins.append(DependencyPin(d['dependency_id'],d['semantic_owner'],SourceContext(d['source_context']),ReuseMode(d['reuse_mode']),d['relative_root'],tuple(d['file_globs']),int(d['expected_file_count']),d['expected_aggregate_sha256'],d['exact_version'],False))
    return policy,tuple(pins)
