from __future__ import annotations
import math, statistics
from .models import SurfaceStabilityResult, ParameterNeighbor
from .hashing import stable_id

def build_knn_edges(parameter_vectors: dict[str, tuple[float, ...]], k: int = 4) -> tuple[ParameterNeighbor, ...]:
    if k < 1 or len(parameter_vectors) < 2:
        raise ValueError("parameter surface requires at least two trials and k>=1")
    ids=sorted(parameter_vectors); dims={len(parameter_vectors[x]) for x in ids}
    if len(dims)!=1 or next(iter(dims))<1:
        raise ValueError("aligned non-empty parameter vectors required")
    edges={}
    for a in ids:
        distances=[]
        for b in ids:
            if a==b: continue
            d=math.sqrt(sum((x-y)**2 for x,y in zip(parameter_vectors[a],parameter_vectors[b])))
            distances.append((d,b))
        for d,b in sorted(distances)[:min(k,len(distances))]:
            key=tuple(sorted((a,b))); edges[key]=d
    return tuple(ParameterNeighbor(a,b,d).with_hash() for (a,b),d in sorted(edges.items()))

def evaluate_surface_stability(metric_by_trial: dict[str,float],
                               edges: tuple[ParameterNeighbor,...],
                               winner_trial_id: str | None = None) -> SurfaceStabilityResult:
    if len(metric_by_trial)<2 or not edges:
        raise ValueError("surface stability requires metrics and neighbor edges")
    if any(not math.isfinite(v) for v in metric_by_trial.values()):
        raise ValueError("non-finite surface metric")
    winner=(winner_trial_id or max(metric_by_trial,key=lambda t:(metric_by_trial[t],t)))
    if winner not in metric_by_trial: raise ValueError("unknown surface winner")
    winner_value=metric_by_trial[winner]
    neighborhood=[]; rough=[]
    scale=max(1e-12,max(metric_by_trial.values())-min(metric_by_trial.values()))
    for edge in edges:
        a,b=edge.left_trial_id,edge.right_trial_id
        if a not in metric_by_trial or b not in metric_by_trial: continue
        d=max(edge.normalized_distance,1e-12)
        rough.append(abs(metric_by_trial[a]-metric_by_trial[b])/d/scale)
        if a==winner: neighborhood.append(metric_by_trial[b])
        elif b==winner: neighborhood.append(metric_by_trial[a])
    if not neighborhood: raise ValueError("winner has no declared neighbors")
    positive=sum(v>0 for v in neighborhood)/len(neighborhood)
    denom=max(abs(winner_value),1e-12)
    degradation=[max(0.0,(winner_value-v)/denom) for v in neighborhood]
    med=statistics.median(degradation); roughness=sum(rough)/len(rough)
    support=max(0.0,min(1.0,positive*(1.0-min(1.0,med))*(1.0/(1.0+roughness))))
    payload=f"{winner}|{len(neighborhood)}|{positive}|{med}|{roughness}|{support}"
    return SurfaceStabilityResult(winner,len(neighborhood),positive,med,roughness,support,
                                  stable_id("surf",payload))
