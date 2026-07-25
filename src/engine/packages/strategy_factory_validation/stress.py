from __future__ import annotations
import math
from .models import FoldObservation, StressScenario, StressResult
from .enums import StressKind, FoldRole
from .hashing import stable_id, fnv1a64_utf16le

def evaluate_stress(trial_id: str, observations: tuple[FoldObservation,...],
                    scenario: StressScenario, role: FoldRole = FoldRole.TEST) -> StressResult:
    scenario.validate()
    rows=[x for x in observations if x.trial_id==trial_id and x.role==role and not x.ambiguous]
    if not rows: raise ValueError("stress evaluation has no eligible observations")
    retained=list(rows)
    if scenario.kind==StressKind.DETERMINISTIC_TRADE_DROP:
        threshold=int(scenario.drop_fraction*1_000_000)
        retained=[x for x in retained if fnv1a64_utf16le(f"{x.observation_id}|{scenario.seed}")%1_000_000>=threshold]
    elif scenario.kind==StressKind.BEST_TRADE_REMOVAL:
        retained=sorted(retained,key=lambda x:(x.net_r,x.observation_id))
        if scenario.remove_best_count>=len(retained): retained=[]
        elif scenario.remove_best_count: retained=retained[:-scenario.remove_best_count]
    elif scenario.kind==StressKind.CLUSTER_EXCLUSION:
        retained=[x for x in retained if x.cluster_id!=scenario.excluded_cluster_id]
    values=[]
    for row in retained:
        value=row.net_r
        if scenario.kind in (StressKind.ADDITIVE_COST_R,
                              StressKind.ENTRY_DELAY_PENALTY_R,
                              StressKind.EXIT_DELAY_PENALTY_R):
            value-=abs(scenario.additive_penalty_r)
        values.append(value)
    n=len(values); mean=sum(values)/n if n else 0.0; total=sum(values)
    worst=min(values) if values else 0.0; fraction=n/len(rows)
    payload=f"{scenario.scenario_id}|{trial_id}|{n}|{mean}|{total}|{worst}|{fraction}"
    return StressResult(scenario.scenario_id,trial_id,n,mean,total,worst,fraction,
                        stable_id("sres",payload))
