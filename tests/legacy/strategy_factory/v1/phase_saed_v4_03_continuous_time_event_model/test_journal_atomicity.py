import pytest
from dataclasses import replace
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.errors import SequenceError,JournalError,DuplicateConflict
from .helpers import batch

def test_append_commits_atomically(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);r=s.append(batch(stream_nq,nq_events));assert len(r.committed_event_ids)==4 and r.head_sequence==4

def test_sequence_gap_rolls_back(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);bad=(nq_events[0],replace(nq_events[1],source_sequence=3))
    with pytest.raises(SequenceError):s.append(batch(stream_nq,bad))
    assert s.journal.head(stream_nq.stream_id)==0 and not s.journal.all_events()

def test_payload_hash_mismatch_rolls_back(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);bad=(replace(nq_events[0],payload_hash='0'*64),)
    with pytest.raises(JournalError):s.append(batch(stream_nq,bad))
    assert not s.journal.all_events()

def test_idempotent_reappend(stream_nq,nq_events):
    s=ContinuousTimeEventService();s.register_stream(stream_nq);s.append(batch(stream_nq,nq_events));r=s.append(batch(stream_nq,nq_events,'again'));assert len(r.idempotent_event_ids)==4 and r.head_sequence==4
