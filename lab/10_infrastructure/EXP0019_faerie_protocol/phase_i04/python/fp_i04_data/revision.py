from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .constants import M1_MS
from .contracts import DataRevision,M1Bar,RevisionImpact
from .enums import RevisionKind

def dataset_payload_hash(bars):
    return canonical_sha256([(b.canonical_symbol,b.open_utc_ms,b.bar_hash) for b in sorted(bars,key=lambda x:(x.open_utc_ms,x.canonical_symbol))])

def classify_revision(pair_id,current_bars,previous_bars=(),parent_revision_id='NONE',created_utc_ms=0):
    current={(b.canonical_symbol,b.open_utc_ms):b for b in current_bars}; previous={(b.canonical_symbol,b.open_utc_ms):b for b in previous_bars}
    prev_hash=dataset_payload_hash(previous_bars); curr_hash=dataset_payload_hash(current_bars)
    keys=sorted(set(current)|set(previous),key=lambda x:(x[1],x[0]))
    changed=[]; kinds=set(); symbols=set()
    max_prev=max((k[1] for k in previous),default=-1)
    for key in keys:
        old=previous.get(key); new=current.get(key)
        if old is None and new is not None:
            changed.append(key[1]);symbols.add(key[0]);kinds.add(RevisionKind.APPEND if key[1]>max_prev else RevisionKind.LATE_INSERT)
        elif old is not None and new is None:
            changed.append(key[1]);symbols.add(key[0]);kinds.add(RevisionKind.DELETE)
        elif old and new and old.bar_hash!=new.bar_hash:
            changed.append(key[1]);symbols.add(key[0]);kinds.add(RevisionKind.VALUE_CORRECTION)
    if not previous and current: kind=RevisionKind.INITIAL
    elif not changed: kind=RevisionKind.NO_CHANGE
    elif len(kinds)==1: kind=next(iter(kinds))
    else: kind=RevisionKind.VALUE_CORRECTION
    start=min(changed) if changed else (min((b.open_utc_ms for b in current_bars),default=0))
    end=max(changed)+M1_MS if changed else start
    material={'pair_id':pair_id,'parent':parent_revision_id,'kind':kind,'symbols':tuple(sorted(symbols)),'start':start,'end':end,'previous':prev_hash,'current':curr_hash}
    rid=stable_id('FPREV',material,32)
    reason={RevisionKind.INITIAL:'FP_DRC_REVISION_INITIAL',RevisionKind.APPEND:'FP_DRC_REVISION_APPEND',RevisionKind.LATE_INSERT:'FP_DRC_REVISION_LATE_INSERT',RevisionKind.VALUE_CORRECTION:'FP_DRC_REVISION_VALUE_CORRECTION',RevisionKind.DELETE:'FP_DRC_REVISION_DELETE',RevisionKind.NO_CHANGE:'FP_DRC_REVISION_NO_CHANGE',RevisionKind.CONFLICT:'FP_DRC_REVISION_CONFLICT'}[kind]
    return DataRevision(rid,pair_id,parent_revision_id,kind,tuple(sorted(symbols)),start,end,prev_hash,curr_hash,created_utc_ms,reason)

def revision_impact(revision:DataRevision,rows,window_ids=()):
    affected=tuple(r.open_utc_ms for r in rows if revision.affected_start_utc_ms<=r.open_utc_ms<revision.affected_end_utc_ms)
    prefix=[r.row_id for r in rows if r.open_utc_ms<revision.affected_start_utc_ms]
    suffix=[r.row_id for r in rows if r.open_utc_ms>=revision.affected_start_utc_ms]
    return RevisionImpact(revision.revision_id,affected,tuple(sorted(set(window_ids))),canonical_sha256(prefix),canonical_sha256(suffix),'FP_DRC_REVISION_IMPACT_COMPUTED')
