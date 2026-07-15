from __future__ import annotations
from datetime import datetime
from .errors import ResetError
from .canonical import content_hash,stable_id

def _ts(s): return datetime.fromisoformat(str(s).replace('Z','+00:00')).timestamp()

def reset_reasons(previous,current,policy)->tuple[str,...]:
    if previous is None:return ('explicit_restart',)
    out=[]
    if policy.reset_on_context_boundary and previous.context_id!=current.context_id:out.append('context_boundary')
    if policy.reset_on_root_change and previous.root_context_id!=current.root_context_id:out.append('root_context_change')
    if policy.reset_on_domain_change and previous.domain_id!=current.domain_id:out.append('domain_change')
    gap=_ts(current.event_time)-_ts(previous.event_time)
    if gap<0:raise ResetError('negative event-time gap')
    if gap>policy.gap_reset_seconds:out.append('gap_threshold')
    return tuple(sorted(set(out)))

def reset_policy_receipt(policy)->dict:
    material={'reset_on_context_boundary':policy.reset_on_context_boundary,'reset_on_root_change':policy.reset_on_root_change,'reset_on_domain_change':policy.reset_on_domain_change,'reset_on_session_boundary':policy.reset_on_session_boundary,'gap_reset_seconds':policy.gap_reset_seconds,'restart_requires_snapshot_hash':policy.restart_requires_snapshot_hash,'fail_closed_on_corruption':policy.fail_closed_on_corruption}
    return {**material,'policy_id':stable_id('resetpolicy',material),'policy_hash':content_hash(material)}
