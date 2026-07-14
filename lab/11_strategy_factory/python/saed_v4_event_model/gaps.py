from __future__ import annotations
from .models import GapRecord
from .enums import GapSeverity
from .canonical import parse_time

def detect_time_gaps(events,maximum_gap_ms:int):
    grouped={}
    for e in events:grouped.setdefault((e.stream_id,e.subject_id),[]).append(e)
    out=[]
    for (stream,subject),items in grouped.items():
        items=sorted(items,key=lambda x:parse_time(x.event_time))
        for left,right in zip(items,items[1:]):
            dur=int((parse_time(right.event_time)-parse_time(left.event_time)).total_seconds()*1000)
            if dur>maximum_gap_ms:
                sev=GapSeverity.CRITICAL if dur>maximum_gap_ms*10 else (GapSeverity.MATERIAL if dur>maximum_gap_ms*3 else GapSeverity.WARNING)
                out.append(GapRecord(stream,subject,left.event_id,right.event_id,left.event_time,right.event_time,dur,sev,'event-time gap exceeds policy'))
    return tuple(out)
