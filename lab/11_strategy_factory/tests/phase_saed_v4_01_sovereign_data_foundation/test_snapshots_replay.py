import pytest
from saed_v4_data_foundation.models import SovereignRecord,SourceDescriptor
from saed_v4_data_foundation.temporal import BitemporalStamp
from saed_v4_data_foundation.revisions import RevisionStore
from saed_v4_data_foundation.snapshots import build_snapshot
from saed_v4_data_foundation.replay import SnapshotReplayer
from saed_v4_data_foundation.enums import DataRole
from saed_v4_data_foundation.errors import ReplayError
SRC=SourceDescriptor('s','feed','EU','1','1')
def rec(e,n,k,sup=None):return SovereignRecord(e,'x','1',{'x':n},BitemporalStamp('2026-01-01T00:00:00Z',k),SRC,revision_number=n,supersedes_revision_id=sup)
def setup():
 r=RevisionStore();a=rec('a',1,'2026-01-01T00:00:01Z');b=rec('b',1,'2026-01-01T00:00:02Z');r.append(a);r.append(b);return r
def test_snapshot_deterministic():
 r=setup();rows=r.records_as_of('2026-01-01T00:00:03Z');a=build_snapshot(rows,'2026-01-01T00:00:03Z',None,DataRole.DEVELOPMENT,'a'*64);b=build_snapshot(reversed(rows),'2026-01-01T00:00:03Z',None,DataRole.DEVELOPMENT,'a'*64);assert a.snapshot_hash==b.snapshot_hash
def test_replay_exact():
 r=setup();s=build_snapshot(r.records_as_of('2026-01-01T00:00:03Z'),'2026-01-01T00:00:03Z',None,DataRole.DEVELOPMENT,'a'*64);assert SnapshotReplayer(r).replay(s).snapshot_hash==s.snapshot_hash
def test_replay_detects_mismatch():
 r=setup();s=build_snapshot(r.records_as_of('2026-01-01T00:00:03Z'),'2026-01-01T00:00:03Z',None,DataRole.DEVELOPMENT,'a'*64,{'x':1});bad=type(s)(s.snapshot_id,s.artifact_ids,s.row_ids,s.known_as_of,s.event_as_of,s.data_role,s.schema_set_hash,s.lineage_root,s.record_count,{'x':2})
 with pytest.raises(ReplayError): SnapshotReplayer(r).replay(bad)
def test_future_revision_does_not_change_old_snapshot():
 r=setup();old=build_snapshot(r.records_as_of('2026-01-01T00:00:03Z'),'2026-01-01T00:00:03Z',None,DataRole.DEVELOPMENT,'a'*64);head=r.latest('a');r.append(rec('a',2,'2026-01-02T00:00:00Z',head.revision_id));again=build_snapshot(r.records_as_of('2026-01-01T00:00:03Z'),'2026-01-01T00:00:03Z',None,DataRole.DEVELOPMENT,'a'*64);assert old.snapshot_hash==again.snapshot_hash
