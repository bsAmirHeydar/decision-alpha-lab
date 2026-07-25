import pytest
from dataclasses import replace
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.enums import LatePolicy
from saed_v4_event_model.errors import LateEventError
from helpers import batch

def _late_after_head(stream_nq,nq_events):
    e=nq_events[-1]
    return replace(e,source_sequence=5,event_time='2026-01-02T14:29:50Z',known_time='2026-01-02T14:30:03Z',payload={'from':'valid','to':'valid','trigger':'late'},payload_hash='')

def test_accept_flag_records_late(stream_nq,nq_events):
    from saed_v4_event_model.canonical import content_hash
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));e=_late_after_head(stream_nq,nq_events);e=replace(e,payload_hash=content_hash(e.payload));s.append(batch(stream_nq,(e,),'late'));assert s.watermarks.state(stream_nq).late_events==1 and len(s.watermarks.late_records())==1

def test_reject_policy_fails_closed(stream_nq,nq_events):
    from saed_v4_event_model.canonical import content_hash
    s=ContinuousTimeEventService();m=replace(stream_nq,late_policy=LatePolicy.REJECT);s.register_stream(m);s.append(batch(m,nq_events));e=_late_after_head(m,nq_events);e=replace(e,payload_hash=content_hash(e.payload))
    with pytest.raises(LateEventError):s.append(batch(m,(e,),'late'))

def test_quarantine_policy_does_not_advance_head(stream_nq,nq_events):
    from saed_v4_event_model.canonical import content_hash
    s=ContinuousTimeEventService();m=replace(stream_nq,late_policy=LatePolicy.QUARANTINE);s.register_stream(m);s.append(batch(m,nq_events));e=_late_after_head(m,nq_events);e=replace(e,payload_hash=content_hash(e.payload));r=s.append(batch(m,(e,),'late'));assert r.quarantined_event_ids and s.journal.head(m.stream_id)==4
