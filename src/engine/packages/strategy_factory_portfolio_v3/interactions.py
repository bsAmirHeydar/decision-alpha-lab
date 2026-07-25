from __future__ import annotations
from .contracts import InteractionDecision
from .enums import ConflictPolicy,Side
from .canonical import canonical_sha256

def resolve_symbol_conflicts(candidates,policy:ConflictPolicy):
    ids=tuple(sorted(c.candidate_id for c in candidates)); longs=[c for c in candidates if c.side is Side.LONG];shorts=[c for c in candidates if c.side is Side.SHORT]
    if not longs or not shorts:return InteractionDecision('interaction:'+canonical_sha256(ids)[:16],ids,policy,ids,(),longs and Side.LONG or Side.SHORT,('no_direction_conflict',))
    if policy is ConflictPolicy.HEDGE:return InteractionDecision('interaction:'+canonical_sha256(ids)[:16],ids,policy,ids,(),Side.FLAT,('explicit_hedge',))
    if policy is ConflictPolicy.DENY:return InteractionDecision('interaction:'+canonical_sha256(ids)[:16],ids,policy,(),ids,Side.FLAT,('opposite_symbol_direction',))
    l=max(longs,key=lambda x:(x.utility_mean,x.candidate_id));s=max(shorts,key=lambda x:(x.utility_mean,x.candidate_id));winner=l if l.utility_mean>=s.utility_mean else s
    blocked=tuple(sorted(set(ids)-{winner.candidate_id}))
    return InteractionDecision('interaction:'+canonical_sha256(ids)[:16],ids,policy,(winner.candidate_id,),blocked,winner.side,('net_to_higher_utility',))
