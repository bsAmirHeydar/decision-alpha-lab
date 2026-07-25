import pytest
from saed_v4_data_foundation.schema_registry import SchemaRegistry
from saed_v4_data_foundation.revisions import RevisionStore
from saed_v4_data_foundation.quarantine import QuarantineRegistry
from saed_v4_data_foundation.ingestion import IngestionEngine
from saed_v4_data_foundation.models import SovereignRecord,SourceDescriptor,QuarantineRecord
from saed_v4_data_foundation.temporal import BitemporalStamp
from saed_v4_data_foundation.enums import QuarantineReason
from saed_v4_data_foundation.canonical import stable_id
from saed_v4_data_foundation.errors import QuarantineRequired,DataFoundationError
S={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'properties':{'x':{'type':'integer'}},'required':['x']};SRC=SourceDescriptor('s','feed','EU','1','1')
def rec(e='e',payload={'x':1},n=1,sup=None):return SovereignRecord(e,'x','1',payload,BitemporalStamp('2026-01-01T00:00:00Z','2026-01-01T00:00:01Z'),SRC,revision_number=n,supersedes_revision_id=sup)
def engine():
 s=SchemaRegistry();s.register('x','1',S);r=RevisionStore();q=QuarantineRegistry();return IngestionEngine(s,r,q),r,q
def test_atomic_accept():
 e,r,q=engine();res=e.ingest_atomic([rec('a'),rec('b')]);assert len(res.accepted_revision_ids)==2 and not res.quarantined_ids
def test_invalid_batch_commits_none():
 e,r,q=engine();res=e.ingest_atomic([rec('a'),rec('b',{'bad':1})]);assert not res.accepted_revision_ids;assert not r._by_entity;assert len(res.quarantined_ids)==1
def test_blocked_entity():
 e,r,q=engine();x=QuarantineRecord('q','a',QuarantineReason.MANUAL_HOLD,{},'a'*64);q.add(x);res=e.ingest_atomic([rec('a')]);assert res.quarantined_ids
def test_resolve_quarantine():
 e,r,q=engine();x=QuarantineRecord('q','a',QuarantineReason.MANUAL_HOLD,{},'a'*64);q.add(x);q.resolve('q','b'*64);assert not q.is_blocked('a')
def test_invalid_revision_preflight_no_partial():
 e,r,q=engine()
 with pytest.raises(DataFoundationError): e.ingest_atomic([rec('a'),rec('b',n=2)])
 assert not r._by_entity
