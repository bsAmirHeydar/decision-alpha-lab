from __future__ import annotations
from collections import defaultdict
import random, math
from .models import StatisticalSample, ConfidenceInterval
from .enums import IntervalKind

def _percentile(values: list[float], q: float) -> float:
    if not values: return 0.0
    s=sorted(values); pos=q*(len(s)-1); lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi:return s[lo]
    return s[lo]+(s[hi]-s[lo])*(pos-lo)

def cluster_bootstrap_mean_interval(samples: list[StatisticalSample], metric_id: str="mean_net_r",
                                    group_key: str="all=all", iterations: int=2000,
                                    seed: int=17, confidence_level: float=.95) -> ConfidenceInterval:
    filled=[s for s in samples if s.filled]
    clusters=defaultdict(list)
    for s in filled: clusters[s.cluster_id].append(s.net_r)
    keys=sorted(clusters)
    if not keys: raise ValueError("no filled clusters")
    if iterations < 100: raise ValueError("bootstrap iterations too small")
    rng=random.Random(seed); estimates=[]
    for _ in range(iterations):
        vals=[]
        for _ in keys: vals.extend(clusters[rng.choice(keys)])
        estimates.append(sum(vals)/len(vals))
    alpha=(1-confidence_level)/2; estimate=sum(s.net_r for s in filled)/len(filled)
    se=(sum((x-sum(estimates)/len(estimates))**2 for x in estimates)/(len(estimates)-1))**.5
    return ConfidenceInterval(metric_id,group_key,IntervalKind.CLUSTER_BOOTSTRAP_PERCENTILE,
                              confidence_level,estimate,_percentile(estimates,alpha),
                              _percentile(estimates,1-alpha),se,len(keys),seed).with_hash()
