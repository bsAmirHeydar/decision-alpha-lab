import pytest
from dataclasses import replace
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.enums import EventKind
from saed_v4_event_model.canonical import content_hash
from saed_v4_event_model.errors import CorrectionError
from helpers import batch

def test_correction_is_append_only(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));target=nq_events[1];payload={'replacement_payload':{'price':20001.25,'volume':4},'reason':'feed correction'};c=replace(nq_events[-1],source_sequence=5,event_kind=EventKind.CORRECTION,event_time='2026-01-02T14:30:03Z',known_time='2026-01-02T14:30:03.1Z',payload=payload,payload_hash=content_hash(payload),correction_of=target.event_id);s.append(batch(stream_nq,(c,),'corr'));effective=s.journal.effective(stream_nq.twin_id,'2026-01-02T15:00:00Z');assert [e.payload['price'] for e in effective if e.event_kind==EventKind.TRADE]==[20001.25];assert len(s.journal.all_events())==5

def test_unknown_correction_target_rejected(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);payload={'replacement_payload':{'price':1},'reason':'x'};c=replace(nq_events[0],event_kind=EventKind.CORRECTION,payload=payload,payload_hash=content_hash(payload),correction_of='missing')
    with pytest.raises(CorrectionError):s.append(batch(stream_nq,(c,)))
