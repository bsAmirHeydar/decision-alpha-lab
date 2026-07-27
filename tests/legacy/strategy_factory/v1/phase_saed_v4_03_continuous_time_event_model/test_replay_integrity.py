from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.replay import replay_projection
from saed_v4_event_model.integrity import build_integrity_receipt,verify_integrity_receipt
from .helpers import batch

def test_replay_exact(stream_nq,stream_es,nq_events,es_events,projection_def):
    s=ContinuousTimeEventService();[s.register_stream(x) for x in (stream_nq,stream_es)];s.register_projection(projection_def);s.append(batch(stream_nq,nq_events));s.append(batch(stream_es,es_events));events=s.journal.effective(stream_nq.twin_id,'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z');p=s.project(projection_def.projection_name,projection_def.exact_version,'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z');r=replay_projection(projection_def,events,p.known_as_of,p.event_as_of,p.state_hash,s.watermarks.all_states(),tuple(x.event_id for x in s.watermarks.late_records()),());assert r.status=='pass'

def test_integrity_receipt(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));r=build_integrity_receipt(stream_nq.twin_id,s.journal.journal_root(),s.streams.all(),s.watermarks.all_states());assert verify_integrity_receipt(r,s.streams.all(),s.watermarks.all_states())
