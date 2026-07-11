from __future__ import annotations
from .models import MultipleTestingResult
from .hashing import stable_id

def _validate(ids, p_values, alpha):
    if len(ids) != len(p_values) or not ids:
        raise ValueError("hypothesis ids and p-values must be non-empty and aligned")
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate hypothesis id")
    if not 0 < alpha < 1:
        raise ValueError("alpha outside (0,1)")
    if any(p < 0 or p > 1 for p in p_values):
        raise ValueError("p-value outside [0,1]")

def bonferroni(ids, p_values, alpha=0.05):
    ids=tuple(ids); p=tuple(float(x) for x in p_values); _validate(ids,p,alpha)
    m=len(p); adj=tuple(min(1.0,x*m) for x in p)
    return _result("bonferroni",ids,p,adj,tuple(x<=alpha for x in adj),alpha)

def holm(ids, p_values, alpha=0.05):
    ids=tuple(ids); p=tuple(float(x) for x in p_values); _validate(ids,p,alpha)
    order=sorted(range(len(p)), key=lambda i:(p[i],ids[i])); raw=[0.0]*len(p)
    running=0.0
    for rank,i in enumerate(order):
        running=max(running,(len(p)-rank)*p[i]); raw[i]=min(1.0,running)
    rejected=tuple(raw[i]<=alpha for i in range(len(p)))
    return _result("holm",ids,p,tuple(raw),rejected,alpha)

def benjamini_hochberg(ids, p_values, alpha=0.05):
    ids=tuple(ids); p=tuple(float(x) for x in p_values); _validate(ids,p,alpha)
    order=sorted(range(len(p)), key=lambda i:(p[i],ids[i]), reverse=True)
    adj=[1.0]*len(p); running=1.0; m=len(p)
    for reverse_rank,i in enumerate(order):
        rank=m-reverse_rank
        running=min(running,p[i]*m/rank); adj[i]=min(1.0,running)
    rejected=tuple(adj[i]<=alpha for i in range(m))
    return _result("benjamini_hochberg",ids,p,tuple(adj),rejected,alpha)

def _result(method,ids,p,adj,rejected,alpha):
    payload=f"{method}|{ids}|{p}|{adj}|{rejected}|{alpha}"
    return MultipleTestingResult(method,ids,p,adj,rejected,alpha,
                                 stable_id("mt",payload))
