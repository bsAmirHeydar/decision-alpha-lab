from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.gaps import detect_time_gaps
from saed_v4_event_model.enums import AlignmentStatus
from .helpers import batch

def test_async_alignment_complete(stream_nq,stream_es,nq_events,es_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.register_stream(stream_es);s.append(batch(stream_nq,nq_events));s.append(batch(stream_es,es_events));a=s.align(stream_nq.twin_id,('NQ','ES'),'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z',5000);assert a.status==AlignmentStatus.COMPLETE

def test_alignment_missing_subject_unknown(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));a=s.align(stream_nq.twin_id,('NQ','ES'),'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z',5000);assert a.status==AlignmentStatus.UNKNOWN and a.missing_subjects==('ES',)

def test_gap_detection(stream_nq,nq_events):
    gaps=detect_time_gaps(nq_events,400);assert gaps and gaps[0].duration_ms>=500
