"""Dependence-aware uncertainty engines for UCE-I12."""
from __future__ import annotations
from dataclasses import asdict
from math import ceil, sqrt
from typing import Callable, Mapping, Sequence
import numpy as np
from .canonical import canonical_sha256, stable_id
from .contracts import UncertaintyReport
from .errors import PromotionError

def _finite_array(values: Sequence[float]) -> np.ndarray:
    arr=np.asarray(values,dtype=float)
    arr=arr[np.isfinite(arr)]
    if arr.size<2: raise PromotionError("insufficient_samples","at least two finite samples are required")
    return arr

def autocorrelations(values: Sequence[float], max_lag: int | None=None) -> np.ndarray:
    arr=_finite_array(values); n=arr.size
    centered=arr-arr.mean(); denom=float(centered@centered)
    if denom<=0: return np.zeros(min(n-1,max_lag or n-1),dtype=float)
    m=min(n-1,max_lag or max(1,int(sqrt(n))))
    return np.asarray([float(centered[:-lag]@centered[lag:]/denom) for lag in range(1,m+1)])

def effective_sample_size(values: Sequence[float], max_lag: int | None=None) -> float:
    arr=_finite_array(values); rhos=autocorrelations(arr,max_lag)
    positive=[]
    for i in range(0,len(rhos),2):
        pair=float(rhos[i] + (rhos[i+1] if i+1<len(rhos) else 0.0))
        if pair<=0: break
        positive.extend(rhos[i:i+2].tolist())
    tau=max(1.0,1.0+2.0*sum(positive))
    return float(max(1.0,min(len(arr),len(arr)/tau)))

def moving_block_bootstrap(values: Sequence[float], *, block_size:int, iterations:int=2000, confidence:float=.95, seed:int=7, statistic:Callable[[np.ndarray],float]=np.mean) -> Mapping[str,float]:
    arr=_finite_array(values); n=len(arr)
    if not 1<=block_size<=n: raise PromotionError("invalid_block_size","block_size must be in [1,n]")
    if iterations<100: raise PromotionError("insufficient_bootstrap_iterations","at least 100 iterations required")
    starts=np.arange(0,n-block_size+1); blocks=ceil(n/block_size); rng=np.random.default_rng(seed)
    estimates=np.empty(iterations,dtype=float)
    for i in range(iterations):
        chosen=rng.choice(starts,size=blocks,replace=True)
        sample=np.concatenate([arr[s:s+block_size] for s in chosen])[:n]
        estimates[i]=float(statistic(sample))
    alpha=(1-confidence)/2
    return {"estimate":float(statistic(arr)),"lower":float(np.quantile(estimates,alpha)),"upper":float(np.quantile(estimates,1-alpha)),"standard_error":float(np.std(estimates,ddof=1)),"iterations":iterations,"block_size":block_size,"effective_sample_size":effective_sample_size(arr)}

def cluster_bootstrap(values: Sequence[float], clusters: Sequence[str|int], *, iterations:int=2000, confidence:float=.95, seed:int=7, statistic:Callable[[np.ndarray],float]=np.mean) -> Mapping[str,float]:
    arr=np.asarray(values,dtype=float); labels=np.asarray(clusters)
    if len(arr)!=len(labels): raise PromotionError("cluster_length_mismatch","values and clusters must align")
    valid=np.isfinite(arr); arr=arr[valid]; labels=labels[valid]
    unique=sorted(set(labels.tolist()),key=str)
    groups=[arr[labels==label] for label in unique]
    if len(groups)<2: raise PromotionError("insufficient_clusters","at least two clusters required")
    rng=np.random.default_rng(seed); estimates=np.empty(iterations,dtype=float)
    for i in range(iterations):
        picks=rng.integers(0,len(groups),size=len(groups)); estimates[i]=float(statistic(np.concatenate([groups[p] for p in picks])))
    alpha=(1-confidence)/2
    return {"estimate":float(statistic(arr)),"lower":float(np.quantile(estimates,alpha)),"upper":float(np.quantile(estimates,1-alpha)),"standard_error":float(np.std(estimates,ddof=1)),"iterations":iterations,"cluster_count":len(groups),"effective_sample_size":float(len(groups))}

def paired_block_bootstrap(candidate:Sequence[float], baseline:Sequence[float], *, block_size:int, iterations:int=2000, confidence:float=.95, seed:int=7)->Mapping[str,float]:
    x=np.asarray(candidate,dtype=float); y=np.asarray(baseline,dtype=float)
    if x.shape!=y.shape: raise PromotionError("paired_length_mismatch","paired arrays must have equal shape")
    return moving_block_bootstrap(x-y,block_size=block_size,iterations=iterations,confidence=confidence,seed=seed)

def subgroup_uncertainty(values:Sequence[float], groups:Sequence[str], *, block_size:int=2, iterations:int=1000, confidence:float=.95, seed:int=7)->dict[str,dict[str,float]]:
    arr=np.asarray(values,dtype=float); labels=np.asarray(groups)
    if len(arr)!=len(labels): raise PromotionError("subgroup_length_mismatch","values and group labels must align")
    result={}
    for offset,label in enumerate(sorted(set(labels.tolist()))):
        subset=arr[labels==label]
        if np.isfinite(subset).sum()<2: continue
        result[str(label)]=dict(moving_block_bootstrap(subset,block_size=min(block_size,len(subset)),iterations=iterations,confidence=confidence,seed=seed+offset))
    return result

def sequential_confidence(values:Sequence[float], looks:Sequence[int], *, block_size:int=2, iterations:int=1000, overall_confidence:float=.95, seed:int=7)->tuple[Mapping[str,float],...]:
    arr=_finite_array(values); clean=sorted(set(int(x) for x in looks))
    if not clean or clean[-1]>len(arr) or clean[0]<2: raise PromotionError("invalid_sequential_looks","looks must be unique within [2,n]")
    alpha=(1-overall_confidence)/len(clean); conf=1-alpha
    return tuple({"look":look,**moving_block_bootstrap(arr[:look],block_size=min(block_size,look),iterations=iterations,confidence=conf,seed=seed+i)} for i,look in enumerate(clean))

def build_uncertainty_report(values:Sequence[float], *, report_name:str, block_size:int=2, iterations:int=2000, confidence:float=.95, seed:int=7, subgroup_values:Mapping[str,Sequence[float]]|None=None)->UncertaintyReport:
    data=moving_block_bootstrap(values,block_size=block_size,iterations=iterations,confidence=confidence,seed=seed)
    sub={}
    for i,(name,vals) in enumerate(sorted((subgroup_values or {}).items())):
        if len(vals)>=2: sub[name]=dict(moving_block_bootstrap(vals,block_size=min(block_size,len(vals)),iterations=max(500,iterations//2),confidence=confidence,seed=seed+i+1))
    payload={"name":report_name,"data":data,"subgroups":sub,"seed":seed}
    return UncertaintyReport(report_id=stable_id("uncertainty",payload),estimate=data["estimate"],lower=data["lower"],upper=data["upper"],standard_error=data["standard_error"],nominal_sample_size=len(_finite_array(values)),effective_sample_size=data["effective_sample_size"],method="moving_block_bootstrap",confidence=confidence,seed=seed,evidence_hash=canonical_sha256(payload),subgroup_reports=sub)
