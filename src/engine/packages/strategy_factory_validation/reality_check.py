from __future__ import annotations
import math, random
from .models import RealityCheckResult
from .hashing import stable_id

def white_reality_check(excess_returns_by_trial: dict[str, list[float]],
                        bootstrap_iterations: int = 1000,
                        seed: int = 120012) -> RealityCheckResult:
    if len(excess_returns_by_trial) < 2 or bootstrap_iterations < 100:
        raise ValueError("reality check requires multiple trials and at least 100 bootstraps")
    trial_ids=tuple(sorted(excess_returns_by_trial))
    lengths={len(excess_returns_by_trial[t]) for t in trial_ids}
    if len(lengths)!=1 or next(iter(lengths))<3:
        raise ValueError("aligned trial return vectors are required")
    n=next(iter(lengths))
    if any(any(not math.isfinite(x) for x in excess_returns_by_trial[t]) for t in trial_ids):
        raise ValueError("non-finite reality-check return")
    means={t:sum(excess_returns_by_trial[t])/n for t in trial_ids}
    winner=max(trial_ids,key=lambda t:(means[t],t))
    observed=math.sqrt(n)*max(means.values())
    centered={t:[x-means[t] for x in excess_returns_by_trial[t]] for t in trial_ids}
    rng=random.Random(seed); exceed=0
    for _ in range(bootstrap_iterations):
        idx=[rng.randrange(n) for _ in range(n)]
        boot_max=max(math.sqrt(n)*sum(centered[t][i] for i in idx)/n for t in trial_ids)
        if boot_max>=observed: exceed+=1
    p=(exceed+1)/(bootstrap_iterations+1)
    payload=f"{winner}|{observed}|{p}|{bootstrap_iterations}|{seed}"
    return RealityCheckResult(winner,observed,p,bootstrap_iterations,seed,
                              stable_id("wrc",payload))
