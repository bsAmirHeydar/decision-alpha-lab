import pytest
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.enums import ProjectionStatus
from helpers import batch

def test_golden_projection(stream_nq,stream_es,nq_events,es_events,projection_def):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.register_stream(stream_es);s.register_projection(projection_def);s.append(batch(stream_nq,nq_events,'nq'));s.append(batch(stream_es,es_events,'es'));p=s.project(projection_def.projection_name,projection_def.exact_version,'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z');vals={x.field_id:x.value for x in p.values};assert p.status==ProjectionStatus.COMPLETE;assert vals['nq_last_bid']==20000.0;assert vals['nq_trade_count']==1;assert vals['es_relation_score']==0.8;assert vals['context_state']=='valid'

def test_future_suffix_does_not_change_past_projection(stream_nq,nq_events,projection_def):
    from dataclasses import replace
    from saed_v4_event_model.canonical import content_hash
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.register_projection(projection_def);s.append(batch(stream_nq,nq_events));p1=s.project(projection_def.projection_name,projection_def.exact_version,'2026-01-02T14:30:02.5Z','2026-01-02T14:30:02Z');payload={'price':99999.0,'volume':1};future=replace(nq_events[1],source_sequence=5,event_time='2026-01-02T14:35:00Z',known_time='2026-01-02T14:35:00.1Z',payload=payload,payload_hash=content_hash(payload));s.append(batch(stream_nq,(future,),'future'));p2=s.project(projection_def.projection_name,projection_def.exact_version,'2026-01-02T14:30:02.5Z','2026-01-02T14:30:02Z');assert p1.state_hash==p2.state_hash
