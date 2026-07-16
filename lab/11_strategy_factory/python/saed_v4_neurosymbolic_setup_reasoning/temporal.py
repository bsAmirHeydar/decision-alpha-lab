from __future__ import annotations
from .contracts import TemporalLogicContract
from .errors import TemporalLogicError

def compile_temporal(mapping):
    o=TemporalLogicContract.from_mapping(mapping);return o

def evaluate_clause(clause,events,decision_time,contract):
    keys={'clause_id','operator','predicate_id','secondary_predicate_id','window','minimum_count'}
    if set(clause)!=keys:raise TemporalLogicError('temporal clause fields mismatch')
    op=clause['operator'];window=int(clause['window']);minimum=int(clause['minimum_count'])
    if op not in contract.operators or window<1 or window>contract.max_window:raise TemporalLogicError('temporal clause outside contract')
    safe=[e for e in events if e['known_time']<=decision_time and e['event_time']<=decision_time]
    safe=sorted(safe,key=lambda x:(x['event_time'],x['event_id']))[-contract.max_history:]
    lo=decision_time-window; recent=[e for e in safe if e['event_time']>=lo]
    a=[e for e in recent if clause['predicate_id'] in e['predicate_ids']]
    b=[e for e in recent if clause['secondary_predicate_id'] and clause['secondary_predicate_id'] in e['predicate_ids']]
    if op=='always':return bool(recent) and len(a)==len(recent)
    if op=='eventually_within':return len(a)>=max(1,minimum)
    if op=='count_within':return len(a)>=minimum
    if op=='holds_for':
        times=sorted(e['event_time'] for e in a);return len(times)>=minimum and times[-1]-times[0]>=window-1
    if op=='precedes':return bool(a and b) and min(e['event_time'] for e in a)<max(e['event_time'] for e in b)
    if op=='until':
        if not b:return False
        stop=min(e['event_time'] for e in b);return all(clause['predicate_id'] in e['predicate_ids'] for e in recent if e['event_time']<stop)
    raise TemporalLogicError('unsupported temporal operator')
