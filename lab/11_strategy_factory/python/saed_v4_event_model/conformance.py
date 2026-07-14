from __future__ import annotations
from .canonical import content_hash
from .enums import EventKind,ClockDomain,LatePolicy,ProjectionReducer
from .models import *
from .service import ContinuousTimeEventService

def source(d):return EventSourceDescriptor(d['source_id'],d['source_version'],ClockDomain(d['clock_domain']),d['source_hash'],d['trusted'],d.get('timezone','UTC'),d.get('metadata',{}))
def manifest(d):return EventStreamManifest(d['stream_id'],d['exact_version'],d['twin_id'],source(d['source']),tuple(d['subject_ids']),tuple(EventKind(x) for x in d['accepted_kinds']),d['source_priority'],d['maximum_lateness_ms'],LatePolicy(d['late_policy']),d['schema_version'],EventAuthorityBoundary(**d.get('authority',{})),tuple(d.get('limitations',())))
def event(d):return EventEnvelope(d['stream_id'],d['stream_version'],d['twin_id'],d['source_id'],d['source_sequence'],EventKind(d['event_kind']),d['subject_id'],d['event_time'],d['known_time'],d['payload'],d.get('payload_hash') or content_hash(d['payload']),d['source_hash'],d.get('correlation_id'),d.get('correction_of'),tuple(d.get('tags',())))
def projection(d):
    fields=tuple(ProjectionFieldDefinition(x['field_id'],tuple(EventKind(k) for k in x['event_kinds']),x['payload_path'],ProjectionReducer(x['reducer']),x.get('window_seconds'),tuple(x.get('subject_ids',())),x.get('required',False),x.get('maximum_staleness_ms'),x.get('default')) for x in d['fields'])
    return EventProjectionDefinition(d['projection_name'],d['exact_version'],d['twin_id'],fields,d['description'],tuple(d.get('limitations',())))
def run_vector(v):
    try:
        s=ContinuousTimeEventService();m=manifest(v['stream']);s.register_stream(m)
        if 'projection' in v:s.register_projection(projection(v['projection']))
        ev=tuple(event(x) for x in v.get('events',[]));batch=EventBatch(v['batch_id'],m.stream_id,m.exact_version,ev,content_hash([x.envelope_hash for x in ev]));res=s.append(batch)
        if v.get('expect_error'):return {'name':v['name'],'passed':False,'observed':'no_error'}
        observed={'disposition':res.disposition.value,'committed':len(res.committed_event_ids),'head_sequence':res.head_sequence}
        if 'projection' in v:
            p=s.project(v['projection']['projection_name'],v['projection']['exact_version'],v['known_as_of'],v['event_as_of']);observed['projection_status']=p.status.value;observed['state_hash']=p.state_hash
        expected=v.get('expected',{});passed=all(observed.get(k)==val for k,val in expected.items())
        return {'name':v['name'],'passed':passed,'observed':observed,'expected':expected}
    except Exception as e:
        return {'name':v['name'],'passed':bool(v.get('expect_error')),'observed':type(e).__name__,'expected':'error' if v.get('expect_error') else v.get('expected',{})}
def run_vectors(vectors):return [run_vector(v) for v in vectors]
