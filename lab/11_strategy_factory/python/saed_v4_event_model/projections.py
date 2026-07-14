from __future__ import annotations
from .models import ProjectionValue,EventStateProjection
from .enums import ProjectionStatus
from .canonical import content_hash,parse_time
from .reducers import payload_get,reduce_values
from .temporal import age_ms

def build_projection(definition,events,known_as_of,event_as_of,watermarks=(),late_event_ids=(),gaps=(),sequence=1):
    values=[];included=set();missing=[];stale=[]
    for field in sorted(definition.fields,key=lambda x:x.field_id):
        selected=[]
        for e in events:
            if e.event_kind not in field.event_kinds:continue
            if field.subject_ids and e.subject_id not in field.subject_ids:continue
            if field.window_seconds is not None and (parse_time(event_as_of)-parse_time(e.event_time)).total_seconds()>field.window_seconds:continue
            try:v=payload_get(dict(e.payload),field.payload_path)
            except KeyError:continue
            selected.append((e,v))
        selected.sort(key=lambda x:(parse_time(x[0].event_time),parse_time(x[0].known_time),x[0].event_id))
        if not selected:
            values.append(ProjectionValue(field.field_id,field.default,(),None,False,True));
            if field.required:missing.append(field.field_id)
            continue
        val=reduce_values(field.reducer,selected,event_as_of,field.window_seconds);ids=tuple(x[0].event_id for x in selected);included.update(ids);last=selected[-1][0].event_time
        is_stale=field.maximum_staleness_ms is not None and age_ms(last,event_as_of)>field.maximum_staleness_ms
        if is_stale:stale.append(field.field_id)
        values.append(ProjectionValue(field.field_id,val,ids,last,is_stale,False))
    status=ProjectionStatus.UNKNOWN if missing else (ProjectionStatus.DEGRADED if stale or gaps else ProjectionStatus.COMPLETE)
    payload={'projection_id':definition.projection_id,'projection_version':definition.exact_version,'twin_id':definition.twin_id,'known_as_of':known_as_of,'event_as_of':event_as_of,'status':status.value,'values':[{'field_id':v.field_id,'value':v.value,'event_ids':list(v.event_ids),'last_event_time':v.last_event_time,'stale':v.stale,'missing':v.missing} for v in values],'included_event_ids':sorted(included),'gap_ids':sorted(g.gap_id for g in gaps)}
    return EventStateProjection(definition.projection_id,definition.exact_version,definition.twin_id,known_as_of,event_as_of,status,tuple(values),tuple(sorted(included)),tuple(sorted(late_event_ids)),tuple(sorted(g.gap_id for g in gaps)),tuple(sorted(w.watermark_id for w in watermarks)),sequence,content_hash(payload))
