from __future__ import annotations
from decimal import Decimal as D
from .golden import *
from .cube import CounterfactualOutcomeCubeBuilder
from .labels import LabelCompiler
from .splits import build_purged_embargoed_plan
from .canonical import sha256

def run_conformance()->dict:
    anchors=golden_anchors(6); scenarios=golden_scenarios(); tasks=golden_tasks(); cb=CounterfactualOutcomeCubeBuilder(); lc=LabelCompiler()
    cubes=[cb.build(a,golden_treatments(a),golden_path(a),scenarios,[300_000]) for a in anchors]
    labels=[l for c in cubes for t in tasks for l in lc.compile(c,t,max(x.maturity.observation_end_ms for x in c.cells))]
    split=build_purged_embargoed_plan(anchors,fold_count=3,purge_ms=60_000,embargo_ms=60_000)
    repeated=[cb.build(a,golden_treatments(a),golden_path(a),scenarios,[300_000]).cube_hash for a in anchors]
    first=[c.cube_hash for c in cubes]
    return {"accepted":first==repeated,"anchor_count":len(anchors),"cube_count":len(cubes),"cell_count":sum(len(c.cells) for c in cubes),"label_count":len(labels),"split_assignment_count":len(split.assignments),"cube_set_hash":sha256(first),"label_set_hash":sha256([x.to_dict() for x in labels]),"split_plan_hash":split.plan_hash}
