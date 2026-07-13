"""Deterministic null and negative-control construction."""
from __future__ import annotations
from typing import Mapping, Sequence
import numpy as np
from .canonical import canonical_sha256, stable_id
from .contracts import NullControlResult
from .enums import EvidenceStatus, NullKind
from .errors import PromotionError

def _arrays(observed:Sequence[float], null:Sequence[float])->tuple[np.ndarray,np.ndarray]:
    x=np.asarray(observed,dtype=float); y=np.asarray(null,dtype=float)
    if x.shape!=y.shape: raise PromotionError("null_length_mismatch","observed and null arrays must align")
    valid=np.isfinite(x)&np.isfinite(y); x=x[valid]; y=y[valid]
    if len(x)<2: raise PromotionError("insufficient_null_samples","at least two paired samples required")
    return x,y

def random_direction(values:Sequence[float], *, seed:int=7)->np.ndarray:
    arr=np.asarray(values,dtype=float); rng=np.random.default_rng(seed); return arr*rng.choice((-1.0,1.0),size=len(arr))

def label_permutation(values:Sequence[float], *, seed:int=7)->np.ndarray:
    arr=np.asarray(values,dtype=float); rng=np.random.default_rng(seed); return arr[rng.permutation(len(arr))]

def delayed_trigger(values:Sequence[float], delay:int)->np.ndarray:
    arr=np.asarray(values,dtype=float)
    if delay<1 or delay>=len(arr): raise PromotionError("invalid_delay","delay must be in [1,n-1]")
    return np.concatenate([np.zeros(delay),arr[:-delay]])

def matched_control(values:Sequence[float], match_keys:Sequence[str], *, seed:int=7)->np.ndarray:
    arr=np.asarray(values,dtype=float); keys=np.asarray(match_keys)
    if len(arr)!=len(keys): raise PromotionError("match_key_length_mismatch","match keys must align")
    out=np.empty_like(arr); rng=np.random.default_rng(seed)
    for key in sorted(set(keys.tolist())):
        idx=np.flatnonzero(keys==key); out[idx]=arr[rng.permutation(idx)]
    return out

def paired_sign_permutation_p(observed:Sequence[float], null:Sequence[float], *, iterations:int=5000, seed:int=7)->float:
    x,y=_arrays(observed,null); d=x-y; stat=float(np.mean(d)); rng=np.random.default_rng(seed); exceed=0
    for _ in range(iterations): exceed += int(np.mean(d*rng.choice((-1.0,1.0),size=len(d)))>=stat)
    return float((1+exceed)/(iterations+1))

def evaluate_null(kind:NullKind, observed:Sequence[float], null:Sequence[float], *, alpha:float=.05, iterations:int=5000, seed:int=7, control_name:str|None=None)->NullControlResult:
    x,y=_arrays(observed,null); obs=float(np.mean(x)); base=float(np.mean(y)); uplift=obs-base; p=paired_sign_permutation_p(x,y,iterations=iterations,seed=seed); status=EvidenceStatus.PASS if uplift>0 and p<=alpha else EvidenceStatus.FAIL
    payload={"kind":kind,"observed":obs,"null":base,"uplift":uplift,"p":p,"n":len(x),"seed":seed}
    return NullControlResult(control_id=stable_id("null",{"name":control_name or kind.value,**payload}),kind=kind,observed_metric=obs,null_metric=base,uplift=uplift,p_value=p,status=status,sample_count=len(x),evidence_hash=canonical_sha256(payload),details={"iterations":iterations,"alpha":alpha,"seed":seed})

def mandatory_null_coverage(results:Sequence[NullControlResult], mandatory:Sequence[NullKind])->Mapping[str,object]:
    by_kind={r.kind:r for r in results}; missing=[k.value for k in mandatory if k not in by_kind]; failed=[k.value for k in mandatory if k in by_kind and by_kind[k].status is not EvidenceStatus.PASS]
    payload={"missing":missing,"failed":failed,"present":sorted(k.value for k in by_kind)}
    return {"passed":not missing and not failed,**payload,"evidence_hash":canonical_sha256(payload)}
