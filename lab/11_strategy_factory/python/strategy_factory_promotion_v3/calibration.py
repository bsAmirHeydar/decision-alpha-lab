"""Calibration, conformal coverage and decision-quality evaluation."""
from __future__ import annotations
from math import log
from typing import Mapping, Sequence
import numpy as np
from .canonical import canonical_sha256, stable_id
from .contracts import CalibrationReport
from .errors import PromotionError

def _binary(y_true:Sequence[int], probabilities:Sequence[float])->tuple[np.ndarray,np.ndarray]:
    y=np.asarray(y_true,dtype=float); p=np.asarray(probabilities,dtype=float)
    if y.shape!=p.shape or len(y)<2: raise PromotionError("invalid_calibration_arrays","labels and probabilities must align with >=2 rows")
    if np.any(~np.isfinite(y)) or np.any(~np.isfinite(p)) or np.any((p<0)|(p>1)) or np.any(~np.isin(y,[0,1])): raise PromotionError("invalid_binary_calibration_values","invalid labels/probabilities")
    return y,p

def brier_score(y_true,probabilities)->float:
    y,p=_binary(y_true,probabilities); return float(np.mean((p-y)**2))

def log_loss(y_true,probabilities,eps:float=1e-12)->float:
    y,p=_binary(y_true,probabilities); p=np.clip(p,eps,1-eps); return float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p)))

def reliability_bins(y_true,probabilities,*,bins:int=10)->tuple[Mapping[str,float],...]:
    y,p=_binary(y_true,probabilities)
    if bins<2: raise PromotionError("invalid_calibration_bins","bins must be >=2")
    edges=np.linspace(0,1,bins+1); rows=[]
    for i in range(bins):
        mask=(p>=edges[i]) & ((p<=edges[i+1]) if i==bins-1 else (p<edges[i+1]))
        rows.append({"bin":i,"lower":float(edges[i]),"upper":float(edges[i+1]),"count":int(mask.sum()),"mean_probability":float(p[mask].mean()) if mask.any() else 0.0,"event_rate":float(y[mask].mean()) if mask.any() else 0.0})
    return tuple(rows)

def expected_calibration_error(y_true,probabilities,*,bins:int=10)->float:
    rows=reliability_bins(y_true,probabilities,bins=bins); n=sum(r["count"] for r in rows); return float(sum(r["count"]/n*abs(r["mean_probability"]-r["event_rate"]) for r in rows))

def conformal_coverage(lower:Sequence[float], upper:Sequence[float], observed:Sequence[float])->float:
    lo=np.asarray(lower,dtype=float); hi=np.asarray(upper,dtype=float); y=np.asarray(observed,dtype=float)
    if lo.shape!=hi.shape or lo.shape!=y.shape or len(y)<1 or np.any(lo>hi): raise PromotionError("invalid_conformal_intervals","interval arrays invalid")
    return float(np.mean((y>=lo)&(y<=hi)))

def decision_curve(y_true,probabilities,thresholds:Sequence[float])->tuple[Mapping[str,float],...]:
    y,p=_binary(y_true,probabilities); n=len(y); rows=[]
    for t in thresholds:
        if not 0<t<1: raise PromotionError("invalid_decision_threshold","thresholds must be in (0,1)")
        pred=p>=t; tp=float(np.sum(pred&(y==1))); fp=float(np.sum(pred&(y==0))); benefit=tp/n-fp/n*(t/(1-t)); rows.append({"threshold":float(t),"net_benefit":benefit,"selection_rate":float(np.mean(pred))})
    return tuple(rows)

def utility_by_threshold(outcomes:Sequence[float],probabilities:Sequence[float],thresholds:Sequence[float])->tuple[Mapping[str,float],...]:
    r=np.asarray(outcomes,dtype=float); p=np.asarray(probabilities,dtype=float)
    if r.shape!=p.shape: raise PromotionError("utility_length_mismatch","outcomes and probabilities must align")
    rows=[]
    for t in thresholds:
        mask=p>=t; rows.append({"threshold":float(t),"coverage":float(mask.mean()),"utility":float(r[mask].mean()) if mask.any() else 0.0,"total_utility":float(r[mask].sum())})
    return tuple(rows)

def abstention_metrics(y_true,probabilities,*,low:float=.4,high:float=.6)->Mapping[str,float]:
    y,p=_binary(y_true,probabilities)
    if not 0<=low<high<=1: raise PromotionError("invalid_abstention_band","invalid abstention band")
    accepted=(p<=low)|(p>=high); pred=p>=.5; return {"coverage":float(accepted.mean()),"accuracy_when_accepted":float(np.mean(pred[accepted]==y[accepted])) if accepted.any() else 0.0,"abstention_rate":float(1-accepted.mean())}

def risk_tier_calibration(y_true,probabilities,tiers:Sequence[str])->Mapping[str,object]:
    y,p=_binary(y_true,probabilities); t=np.asarray(tiers)
    if len(t)!=len(y): raise PromotionError("tier_length_mismatch","risk tiers must align")
    rows={}; errors=[]
    for tier in sorted(set(t.tolist())):
        mask=t==tier; predicted=float(p[mask].mean()); actual=float(y[mask].mean()); rows[str(tier)]={"count":int(mask.sum()),"predicted":predicted,"actual":actual,"absolute_error":abs(predicted-actual)}; errors.append(abs(predicted-actual))
    return {"tiers":rows,"mean_absolute_error":float(np.mean(errors))}

def build_calibration_report(y_true,probabilities,*, conformal_lower:Sequence[float], conformal_upper:Sequence[float], conformal_observed:Sequence[float], target_coverage:float, outcomes:Sequence[float], risk_tiers:Sequence[str], report_name:str="candidate", bins:int=10)->CalibrationReport:
    b=brier_score(y_true,probabilities); ll=log_loss(y_true,probabilities); ece=expected_calibration_error(y_true,probabilities,bins=bins); coverage=conformal_coverage(conformal_lower,conformal_upper,conformal_observed); curves=decision_curve(y_true,probabilities,(.25,.5,.75)); abst=abstention_metrics(y_true,probabilities); tiers=risk_tier_calibration(y_true,probabilities,risk_tiers); best=max(r["net_benefit"] for r in curves)
    payload={"brier":b,"log_loss":ll,"ece":ece,"coverage":coverage,"target":target_coverage,"net_benefit":best,"abstention":abst,"tiers":tiers,"utility":utility_by_threshold(outcomes,probabilities,(.25,.5,.75))}
    return CalibrationReport(report_id=stable_id("calibration",{"name":report_name,**payload}),brier_score=b,log_loss=ll,expected_calibration_error=ece,conformal_coverage=coverage,target_coverage=target_coverage,decision_net_benefit=best,abstention_coverage=abst["coverage"],risk_tier_error=tiers["mean_absolute_error"],evidence_hash=canonical_sha256(payload),details=payload)
