"""Winner-overfit diagnostics: PBO/CSCV, deflation, reality check and SPA."""
from __future__ import annotations
from itertools import combinations
from math import erf, log, sqrt
from typing import Mapping
import numpy as np
from .canonical import canonical_sha256
from .errors import PromotionError

def _cdf(x:float)->float: return .5*(1+erf(x/sqrt(2)))

def probabilistic_performance(observed:float, benchmark:float, sample_count:int, skewness:float=0.0, excess_kurtosis:float=0.0)->float:
    if sample_count<=1: return .5
    variance=max(1e-12,(1-skewness*observed+((excess_kurtosis+2)/4)*observed**2)/(sample_count-1))
    return float(_cdf((observed-benchmark)/sqrt(variance)))

def expected_maximum(trial_count:int, trial_std:float=1.0)->float:
    if trial_count<=1:return 0.0
    gamma=.5772156649015329; a=sqrt(2*log(trial_count)); b=a-(log(log(trial_count))+log(4*np.pi))/(2*a)
    return float(trial_std*(b+gamma/a))

def deflated_performance(observed:float, *, sample_count:int, total_choice_count:int, skewness:float=0.0, excess_kurtosis:float=0.0, trial_std:float=1.0)->Mapping[str,float]:
    if total_choice_count<1: raise PromotionError("empty_trial_universe","trial count must be positive")
    benchmark=expected_maximum(total_choice_count,trial_std)
    result={"observed":float(observed),"benchmark":benchmark,"probability":probabilistic_performance(observed,benchmark,sample_count,skewness,excess_kurtosis),"sample_count":sample_count,"total_choice_count":total_choice_count}
    return {**result,"evidence_hash":canonical_sha256(result)}

def pbo_cscv(performance_matrix, *, max_combinations:int=5000, seed:int=7)->Mapping[str,object]:
    matrix=np.asarray(performance_matrix,dtype=float)
    if matrix.ndim!=2 or matrix.shape[0]<4 or matrix.shape[1]<2: raise PromotionError("invalid_cscv_matrix","requires >=4 blocks and >=2 candidates")
    blocks=matrix.shape[0]
    if blocks%2: raise PromotionError("odd_cscv_blocks","CSCV requires even block count")
    combos=list(combinations(range(blocks),blocks//2)); rng=np.random.default_rng(seed)
    if len(combos)>max_combinations:
        idx=np.sort(rng.choice(len(combos),size=max_combinations,replace=False)); combos=[combos[i] for i in idx]
    logits=[]; failure=0; winners=[]
    for train in combos:
        test=tuple(i for i in range(blocks) if i not in set(train)); train_scores=np.nanmean(matrix[list(train)],axis=0); winner=int(np.nanargmax(train_scores)); test_scores=np.nanmean(matrix[list(test)],axis=0)
        order=np.argsort(np.argsort(test_scores,kind="mergesort"),kind="mergesort"); percentile=(order[winner]+1)/matrix.shape[1]; clipped=float(np.clip(percentile,1e-9,1-1e-9)); logits.append(log(clipped/(1-clipped))); failure+=int(percentile<=.5); winners.append(winner)
    payload={"pbo":failure/len(logits),"median_logit":float(np.median(logits)),"combination_count":len(logits),"winner_counts":{str(i):winners.count(i) for i in sorted(set(winners))}}
    return {**payload,"evidence_hash":canonical_sha256(payload)}

def _block_indices(n:int, block_size:int, rng)->np.ndarray:
    starts=np.arange(0,n-block_size+1); count=int(np.ceil(n/block_size)); chosen=rng.choice(starts,size=count,replace=True); return np.concatenate([np.arange(s,s+block_size) for s in chosen])[:n]

def white_reality_check(returns_matrix, *, iterations:int=2000, block_size:int=5, seed:int=7)->Mapping[str,float]:
    matrix=np.asarray(returns_matrix,dtype=float)
    if matrix.ndim!=2 or matrix.shape[0]<2 or matrix.shape[1]<1: raise PromotionError("invalid_returns_matrix","matrix must be 2D")
    n,k=matrix.shape; centered=matrix-np.nanmean(matrix,axis=0,keepdims=True); observed=float(np.nanmax(np.nanmean(matrix,axis=0))); rng=np.random.default_rng(seed); maxima=np.empty(iterations)
    for i in range(iterations): maxima[i]=float(np.nanmax(np.nanmean(centered[_block_indices(n,min(block_size,n),rng)],axis=0)))
    p=float((1+np.sum(maxima>=observed))/(iterations+1)); payload={"observed_best_mean":observed,"p_value":p,"iterations":iterations,"candidate_count":k}
    return {**payload,"evidence_hash":canonical_sha256(payload)}

def spa_test(returns_matrix, *, benchmark=0.0, iterations:int=2000, block_size:int=5, seed:int=7)->Mapping[str,float]:
    matrix=np.asarray(returns_matrix,dtype=float)-float(benchmark)
    if matrix.ndim!=2 or matrix.shape[0]<3 or matrix.shape[1]<1: raise PromotionError("invalid_spa_matrix","SPA matrix requires >=3 rows")
    n,k=matrix.shape; means=np.nanmean(matrix,axis=0); std=np.nanstd(matrix,axis=0,ddof=1)/sqrt(n); observed=float(np.nanmax(means/np.maximum(std,1e-12)))
    centered=matrix-np.maximum(means,0.0); rng=np.random.default_rng(seed); maxima=np.empty(iterations)
    for i in range(iterations):
        sample=centered[_block_indices(n,min(block_size,n),rng)]; sm=np.nanmean(sample,axis=0); ss=np.nanstd(sample,axis=0,ddof=1)/sqrt(n); maxima[i]=float(np.nanmax(sm/np.maximum(ss,1e-12)))
    p=float((1+np.sum(maxima>=observed))/(iterations+1)); payload={"observed_studentized_max":observed,"p_value":p,"iterations":iterations,"candidate_count":k}
    return {**payload,"evidence_hash":canonical_sha256(payload)}
