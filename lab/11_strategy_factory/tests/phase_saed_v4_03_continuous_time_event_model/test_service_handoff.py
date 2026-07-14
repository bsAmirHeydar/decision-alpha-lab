from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.integrity import build_integrity_receipt
from saed_v4_event_model.handoff import build_v4_04_handoff
from saed_v4_event_model.telemetry import build_telemetry
from helpers import batch

def test_handoff_is_bounded(stream_nq,stream_es,nq_events,es_events,projection_def):
    s=ContinuousTimeEventService();[s.register_stream(x) for x in (stream_nq,stream_es)];s.register_projection(projection_def);s.append(batch(stream_nq,nq_events));s.append(batch(stream_es,es_events));p=s.project(projection_def.projection_name,projection_def.exact_version,'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z');r=build_integrity_receipt(stream_nq.twin_id,s.journal.journal_root(),s.streams.all(),s.watermarks.all_states(),p);h=build_v4_04_handoff('c'*64,s.streams.all(),p,r,['fixture only']);assert not any(h['authority'].values()) and h['next_phase']=='SAED_V4_04'

def test_telemetry_has_no_authority(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));t=build_telemetry(stream_nq.twin_id,s.journal,s.watermarks,(),'2026-01-02T15:00:00Z');assert not any(t['authority'].values())
