import pytest
from saed_v4_data_foundation.models import SovereignRecord,SourceDescriptor
from saed_v4_data_foundation.temporal import BitemporalStamp
from saed_v4_data_foundation.revisions import RevisionStore
from saed_v4_data_foundation.errors import TemporalIntegrityError
SRC=SourceDescriptor('s','feed','EU','1','1')
def rec(n,known,sup=None,value=1): return SovereignRecord('e','x','1',{'x':value},BitemporalStamp('2026-01-01T00:00:00Z',known),SRC,revision_number=n,supersedes_revision_id=sup)
def test_append_latest_asof():
 s=RevisionStore();r1=rec(1,'2026-01-01T00:00:01Z');s.append(r1);r2=rec(2,'2026-01-01T00:00:05Z',r1.revision_id,2);s.append(r2);assert s.latest('e')==r2;assert s.as_of('e','2026-01-01T00:00:04Z')==r1
def test_future_suffix_invariance():
 s=RevisionStore();r1=rec(1,'2026-01-01T00:00:01Z');s.append(r1);before=s.as_of('e','2026-01-01T00:00:02Z');r2=rec(2,'2026-01-02T00:00:00Z',r1.revision_id,9);s.append(r2);assert s.as_of('e','2026-01-01T00:00:02Z')==before
def test_wrong_revision_number():
 s=RevisionStore()
 with pytest.raises(TemporalIntegrityError): s.append(rec(2,'2026-01-01T00:00:01Z'))
def test_wrong_supersedes():
 s=RevisionStore();r1=rec(1,'2026-01-01T00:00:01Z');s.append(r1)
 with pytest.raises(TemporalIntegrityError): s.append(rec(2,'2026-01-01T00:00:02Z','bad'))
def test_known_time_backwards():
 s=RevisionStore();r1=rec(1,'2026-01-01T00:00:05Z');s.append(r1)
 with pytest.raises(TemporalIntegrityError): s.append(rec(2,'2026-01-01T00:00:04Z',r1.revision_id))
def test_idempotent_append():
 s=RevisionStore();r=rec(1,'2026-01-01T00:00:01Z');assert s.append(r)==s.append(r)
