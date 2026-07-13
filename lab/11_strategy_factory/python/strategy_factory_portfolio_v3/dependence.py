from __future__ import annotations
from .contracts import DependenceModel,OpportunityCandidate

def _pair(a,b): return tuple(sorted((a,b)))
def explicit_map(model): return {_pair(e.left_context_id,e.right_context_id):e for e in model.edges}
def correlation(a:OpportunityCandidate,b:OpportunityCandidate,model:DependenceModel):
    if a.context_id==b.context_id:return 1.0
    e=explicit_map(model).get(_pair(a.context_id,b.context_id))
    if e:return e.correlation
    vals=[]
    if a.symbol==b.symbol: vals.append(model.symbol_correlation)
    if a.currency==b.currency: vals.append(model.currency_correlation)
    if a.session_id==b.session_id: vals.append(model.session_correlation)
    if a.anatomy_id==b.anatomy_id: vals.append(model.anatomy_correlation)
    if a.cluster_id==b.cluster_id: vals.append(model.cluster_correlation)
    return max(vals+[model.fallback_correlation])

def marginal_risk(candidate,selected,model):
    if not selected:return candidate.requested_risk
    corr=max(correlation(candidate,x,model) for x in selected)
    return candidate.requested_risk*(1.0+corr)
