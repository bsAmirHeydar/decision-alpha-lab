from __future__ import annotations
import math
from .enums import Severity
from .hashing import stable_id
from .models import (DriftBaseline,DriftObservation,DriftResult,DriftThresholdPolicy,ExecutionDriftObservation,ExecutionDriftPolicy,ExecutionDriftResult)

def _probabilities(counts:tuple[int,...],epsilon:float=1e-12)->tuple[float,...]:
    total=sum(counts)
    if total<=0:return tuple(0.0 for _ in counts)
    raw=[max(epsilon,c/total) for c in counts]; normal=sum(raw)
    return tuple(x/normal for x in raw)

def population_stability_index(expected:tuple[float,...],actual:tuple[float,...],epsilon:float=1e-12)->float:
    if len(expected)!=len(actual): raise ValueError("distribution length mismatch")
    return sum((max(a,epsilon)-max(e,epsilon))*math.log(max(a,epsilon)/max(e,epsilon)) for e,a in zip(expected,actual))

def jensen_shannon(expected:tuple[float,...],actual:tuple[float,...],epsilon:float=1e-12)->float:
    if len(expected)!=len(actual): raise ValueError("distribution length mismatch")
    e=[max(x,epsilon) for x in expected];a=[max(x,epsilon) for x in actual]
    es=sum(e);as_=sum(a);e=[x/es for x in e];a=[x/as_ for x in a];m=[(x+y)/2 for x,y in zip(e,a)]
    kl1=sum(x*math.log(x/y) for x,y in zip(e,m)); kl2=sum(x*math.log(x/y) for x,y in zip(a,m))
    return .5*(kl1+kl2)

def evaluate_drift(b:DriftBaseline,o:DriftObservation,p:DriftThresholdPolicy)->DriftResult:
    if o.baseline_id!=b.baseline_id or o.kind!=b.kind or p.kind!=b.kind: raise ValueError("drift lineage mismatch")
    if len(o.bin_counts)!=len(b.probabilities): raise ValueError("bin mismatch")
    actual=_probabilities(o.bin_counts);psi=population_stability_index(b.probabilities,actual);js=jensen_shannon(b.probabilities,actual)
    z=abs(o.mean-b.mean)/max(b.standard_deviation,1e-12); missing=o.missing_count/max(1,o.sample_count+o.missing_count); invalid=o.invalid_count/max(1,o.sample_count+o.invalid_count)
    sufficient=o.sample_count>=p.minimum_samples; reasons=[];sev=Severity.INFO
    if not sufficient: reasons.append("INSUFFICIENT_SAMPLES")
    if psi>=p.psi_warning: reasons.append("PSI_WARNING");sev=Severity.WARNING
    if js>=p.js_warning: reasons.append("JS_WARNING");sev=max(sev,Severity.WARNING,key=lambda x:list(Severity).index(x))
    if z>=p.mean_z_warning: reasons.append("MEAN_Z_WARNING");sev=Severity.WARNING
    if psi>=p.psi_critical or js>=p.js_critical or z>=p.mean_z_critical or missing>=p.missing_rate_critical or invalid>=p.invalid_rate_critical:
        sev=Severity.CRITICAL
        if psi>=p.psi_critical: reasons.append("PSI_CRITICAL")
        if js>=p.js_critical: reasons.append("JS_CRITICAL")
        if z>=p.mean_z_critical: reasons.append("MEAN_Z_CRITICAL")
        if missing>=p.missing_rate_critical: reasons.append("MISSING_RATE_CRITICAL")
        if invalid>=p.invalid_rate_critical: reasons.append("INVALID_RATE_CRITICAL")
    if not sufficient: sev=Severity.INFO
    rid=stable_id("sf19-drift",b.baseline_id,o.observation_id,p.policy_id,round(psi,12),round(js,12),round(z,12),sev.value)
    return DriftResult(rid,b.baseline_id,o.observation_id,p.policy_id,b.kind,psi,js,z,missing,invalid,sev,sufficient,tuple(reasons))

def evaluate_execution_drift(o:ExecutionDriftObservation,p:ExecutionDriftPolicy)->ExecutionDriftResult:
    reject=o.reject_count/max(1,o.order_count); mismatch=o.mismatch_count/max(1,o.order_count);sufficient=o.order_count>=p.minimum_orders;sev=Severity.INFO;reasons=[]
    if not sufficient:reasons.append("INSUFFICIENT_ORDERS")
    if reject>=p.reject_rate_warning or o.p95_slippage_points>=p.p95_slippage_warning or o.p95_fill_latency_us>=p.p95_fill_latency_warning_us:
        sev=Severity.WARNING; reasons.append("EXECUTION_WARNING")
    if reject>=p.reject_rate_critical or mismatch>=p.mismatch_rate_critical or o.p95_slippage_points>=p.p95_slippage_critical or o.p95_fill_latency_us>=p.p95_fill_latency_critical_us or o.missing_transaction_count>0:
        sev=Severity.CRITICAL; reasons.append("EXECUTION_CRITICAL")
    if not sufficient and o.mismatch_count==0 and o.missing_transaction_count==0: sev=Severity.INFO
    rid=stable_id("sf19-execution-drift",o.observation_id,p.policy_id,reject,mismatch,sev.value)
    return ExecutionDriftResult(rid,o.observation_id,p.policy_id,reject,mismatch,sev,sufficient,tuple(reasons))
