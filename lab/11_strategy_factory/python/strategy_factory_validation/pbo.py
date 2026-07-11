from __future__ import annotations
from itertools import combinations
import math
from collections import Counter
from .models import PBOResult
from .hashing import stable_id

def probability_of_backtest_overfitting(block_returns_by_trial: dict[str, list[float]]) -> PBOResult:
    if len(block_returns_by_trial) < 2:
        raise ValueError("PBO requires at least two trials")
    trial_ids=tuple(sorted(block_returns_by_trial))
    block_counts={len(block_returns_by_trial[t]) for t in trial_ids}
    if len(block_counts)!=1:
        raise ValueError("all trials must have the same block count")
    block_count=block_counts.pop()
    if block_count < 4 or block_count % 2:
        raise ValueError("PBO requires an even block count of at least four")
    if any(any(not math.isfinite(x) for x in block_returns_by_trial[t]) for t in trial_ids):
        raise ValueError("non-finite PBO return")
    half=block_count//2; logits=[]; selected=Counter()
    all_idx=set(range(block_count))
    for train_tuple in combinations(range(block_count),half):
        train=set(train_tuple); test=sorted(all_idx-train)
        train_mean={t:sum(block_returns_by_trial[t][i] for i in train)/half for t in trial_ids}
        winner=max(trial_ids,key=lambda t:(train_mean[t],t)); selected[winner]+=1
        test_mean={t:sum(block_returns_by_trial[t][i] for i in test)/half for t in trial_ids}
        ordered=sorted(trial_ids,key=lambda t:(test_mean[t],t))
        rank=ordered.index(winner)
        omega=(rank+0.5)/len(ordered)
        logits.append(math.log(omega/(1.0-omega)))
    pbo=sum(x<=0.0 for x in logits)/len(logits)
    sorted_logits=sorted(logits); n=len(sorted_logits)
    median=(sorted_logits[n//2] if n%2 else (sorted_logits[n//2-1]+sorted_logits[n//2])/2)
    counts=tuple(sorted(selected.items()))
    payload=f"{pbo}|{median}|{len(logits)}|{counts}"
    return PBOResult(pbo,median,len(logits),counts,stable_id("pbo",payload))
