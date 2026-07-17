from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal,q
from .contracts import require_exact,require_list,require_unique,require_num,require_time_before
from .errors import DependenceError

def freeze_dependence(v:dict,cutoff:str)->dict:
    require_exact(v,["dependence_id","instrument_ids","correlation_matrix","volatility_vector","cluster_map","shrinkage","known_time","synthetic_fixture"]); require_time_before(v["known_time"],cutoff,"dependence.known_time")
    ids=v["instrument_ids"]; require_list(ids,"instrument_ids",4)
    if ids!=sorted(set(ids)): raise DependenceError("instrument ids must be sorted unique")
    m=v["correlation_matrix"]; n=len(ids)
    if not isinstance(m,list) or len(m)!=n or any(not isinstance(r,list) or len(r)!=n for r in m): raise DependenceError("matrix shape invalid")
    for i in range(n):
        if abs(float(m[i][i])-1.0)>1e-12: raise DependenceError("diagonal must be one")
        for k in range(n):
            require_num(m[i][k],"correlation",-1,1)
            if abs(float(m[i][k])-float(m[k][i]))>1e-12: raise DependenceError("matrix not symmetric")
    vols=v["volatility_vector"]
    if set(vols)!=set(ids) or any(float(x)<=0 for x in vols.values()): raise DependenceError("volatility vector invalid")
    if set(v["cluster_map"])!=set(ids): raise DependenceError("cluster map incomplete")
    require_num(v["shrinkage"],"shrinkage",0,1)
    # deterministic Gershgorin lower bound; negative does not prove non-PSD, but extreme invalidity fails closed.
    lower=min(1.0-sum(abs(float(m[i][j])) for j in range(n) if j!=i) for i in range(n))
    body=deepcopy(v); body["gershgorin_lower_bound"]=float(q(lower)); body["dependence_hash"]=content_hash(body); return body

def covariance(dep:dict)->list[list[float]]:
    ids=dep["instrument_ids"]; out=[]
    for i,a in enumerate(ids):
        row=[]
        for j,b in enumerate(ids): row.append(float(q(float(dep["correlation_matrix"][i][j])*float(dep["volatility_vector"][a])*float(dep["volatility_vector"][b]))))
        out.append(row)
    return out
