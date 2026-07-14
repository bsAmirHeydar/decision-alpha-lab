import pytest
from dataclasses import replace
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.errors import TemporalError
from helpers import batch

def test_known_before_event_rejected(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);bad=replace(nq_events[0],known_time='2026-01-02T14:29:59Z')
    with pytest.raises(TemporalError):s.append(batch(stream_nq,(bad,)))

def test_visible_respects_known_and_event_boundaries(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events))
    assert len(s.journal.visible(stream_nq.twin_id,'2026-01-02T14:30:00.700000Z'))==2
    assert len(s.journal.visible(stream_nq.twin_id,'2026-01-02T14:31:00Z','2026-01-02T14:30:00.700000Z'))==2

def test_order_is_event_time_then_known_time(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));ordered=s.journal.visible(stream_nq.twin_id,'2026-01-02T15:00:00Z');assert [x.source_sequence for x in ordered]==[1,2,3,4]
