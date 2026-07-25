"""Stability and market-mechanics stress suite."""
from __future__ import annotations
from typing import Mapping, Sequence
import numpy as np
from .canonical import canonical_sha256, stable_id
from .contracts import StressResult
from .enums import EvidenceStatus, StressKind
from .errors import PromotionError

def metric(values:Sequence[float])->float:
    arr=np.asarray(values,dtype=float); arr=arr[np.isfinite(arr)]
    if len(arr)<1: raise PromotionError("empty_stress_sample","stress sample cannot be empty")
    return float(np.mean(arr))

def evaluate_stress(kind:StressKind, baseline:Sequence[float], stressed:Sequence[float], *, minimum_retention:float=.60, name:str|None=None, details:Mapping[str,object]|None=None)->StressResult:
    b=metric(baseline); s=metric(stressed); retention=s/b if abs(b)>1e-12 else (1.0 if abs(s)<=1e-12 else -1.0); status=EvidenceStatus.PASS if retention>=minimum_retention and s>0 else EvidenceStatus.FAIL
    payload={"kind":kind,"baseline":b,"stressed":s,"retention":retention,"minimum":minimum_retention,"details":dict(details or {})}
    return StressResult(stress_id=stable_id("stress",{"name":name or kind.value,**payload}),kind=kind,baseline_metric=b,stressed_metric=s,relative_retention=float(retention),status=status,evidence_hash=canonical_sha256(payload),details={"minimum_retention":minimum_retention,**dict(details or {})})

def cost_stress(values:Sequence[float], costs:Sequence[float]|float, multiplier:float)->np.ndarray:
    r=np.asarray(values,dtype=float); c=np.asarray(costs,dtype=float)
    if c.ndim==0:c=np.full_like(r,float(c))
    if len(c)!=len(r): raise PromotionError("cost_length_mismatch","costs must be scalar or align")
    if multiplier<1: raise PromotionError("invalid_cost_multiplier","multiplier must be >=1")
    return r-c*(multiplier-1)

def fill_stress(values:Sequence[float], keep_fraction:float, *, seed:int=7)->np.ndarray:
    if not 0<keep_fraction<=1: raise PromotionError("invalid_keep_fraction","keep_fraction must be in (0,1]")
    r=np.asarray(values,dtype=float); rng=np.random.default_rng(seed); keep=rng.random(len(r))<keep_fraction; return np.where(keep,r,0.0)

def trade_drop_stress(values:Sequence[float], drop_fraction:float, *, seed:int=7)->np.ndarray:
    if not 0<=drop_fraction<1: raise PromotionError("invalid_drop_fraction","drop_fraction must be in [0,1)")
    return fill_stress(values,1-drop_fraction,seed=seed)

def best_trade_removal(values:Sequence[float], fraction:float)->np.ndarray:
    if not 0<=fraction<1: raise PromotionError("invalid_removal_fraction","fraction must be in [0,1)")
    r=np.asarray(values,dtype=float).copy(); count=int(np.ceil(len(r)*fraction)); idx=np.argsort(r,kind="mergesort")[-count:] if count else []; r[idx]=0.0; return r

def latency_stress(values:Sequence[float], adverse_per_ms:Sequence[float]|float, latency_ms:float)->np.ndarray:
    r=np.asarray(values,dtype=float); a=np.asarray(adverse_per_ms,dtype=float)
    if a.ndim==0:a=np.full_like(r,float(a))
    if len(a)!=len(r) or latency_ms<0: raise PromotionError("invalid_latency_stress","invalid latency stress inputs")
    return r-a*latency_ms

def parameter_neighborhood(metrics:Mapping[str,float], *, center_key:str, minimum_retention:float=.60)->Mapping[str,object]:
    if center_key not in metrics or len(metrics)<3: raise PromotionError("invalid_parameter_neighborhood","center plus at least two neighbors required")
    center=float(metrics[center_key]); neighbors=[float(v) for k,v in metrics.items() if k!=center_key]; worst=min(neighbors); retention=worst/center if abs(center)>1e-12 else -1.0
    payload={"center":center,"worst_neighbor":worst,"retention":retention,"passed":worst>0 and retention>=minimum_retention,"count":len(metrics)}
    return {**payload,"evidence_hash":canonical_sha256(payload)}

def aggregate_stress(results:Sequence[StressResult])->Mapping[str,object]:
    if not results: raise PromotionError("empty_stress_suite","at least one stress result required")
    failed=[r.kind.value for r in results if r.status is EvidenceStatus.FAIL]; retention=min(r.relative_retention for r in results); payload={"passed":not failed,"failed":failed,"minimum_retention":retention,"count":len(results)}
    return {**payload,"evidence_hash":canonical_sha256(payload)}
