from __future__ import annotations
from .models import AlignmentEntry,AlignmentSnapshot
from .enums import AlignmentStatus
from .canonical import parse_time
from .temporal import age_ms

def align_latest(twin_id,events,subject_ids,known_as_of,event_as_of,maximum_staleness_ms):
    latest={}
    for e in events:
        if e.subject_id not in subject_ids:continue
        old=latest.get(e.subject_id)
        if old is None or parse_time(e.event_time)>parse_time(old.event_time) or (e.event_time==old.event_time and e.event_id>old.event_id):latest[e.subject_id]=e
    entries=[];missing=[];stale=[]
    for s in sorted(subject_ids):
        e=latest.get(s)
        if not e:entries.append(AlignmentEntry(s,None,None,None,False,None));missing.append(s);continue
        age=age_ms(e.event_time,event_as_of);is_stale=age>maximum_staleness_ms
        entries.append(AlignmentEntry(s,e.event_id,e.event_time,age,is_stale,e.payload_hash))
        if is_stale:stale.append(s)
    status=AlignmentStatus.UNKNOWN if missing else (AlignmentStatus.DEGRADED if stale else AlignmentStatus.COMPLETE)
    return AlignmentSnapshot(twin_id,known_as_of,event_as_of,status,tuple(entries),tuple(missing),tuple(stale))
