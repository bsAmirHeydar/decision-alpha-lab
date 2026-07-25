from __future__ import annotations
from typing import Sequence
from .canonical import sha256
from .contracts import *
from .simulator import evaluate_treatment, path_hash

class CounterfactualOutcomeCubeBuilder:
    def build(self, anchor:OpportunityAnchor, treatments:Sequence[TreatmentSibling], path:Sequence[PathObservation], scenarios:Sequence[EconomicScenario], horizons_ms:Sequence[int]) -> OutcomeCube:
        ordered_t=tuple(sorted(treatments,key=lambda x:x.treatment_id))
        ordered_s=tuple(sorted(scenarios,key=lambda x:x.exact_key))
        ordered_h=tuple(sorted(set(int(x) for x in horizons_ms)))
        cells=[]
        for t in ordered_t:
            for s in ordered_s:
                for h in ordered_h:
                    cells.append(evaluate_treatment(anchor,t,path,s,h))
        return OutcomeCube(anchor.opportunity_id,anchor.anchor_hash,path_hash(path),sha256([x.to_dict() for x in ordered_t]),sha256([x.to_dict() for x in ordered_s]),tuple(cells))
