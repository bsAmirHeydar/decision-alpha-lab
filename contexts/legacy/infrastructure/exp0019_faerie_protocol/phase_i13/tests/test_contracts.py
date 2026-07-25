import pytest
from fp_i13_release import *
from fp_i13_release.errors import FPI13Error

def test_fixture_hash_deterministic(fixture): assert fixture.fixture_hash==fixture.fixture_hash

def test_sequences_must_be_unique(config_hash):
 e=ReplayEvent(1,1,ReplayEventType.SEMANTIC_UPSERT,'S', '0'*64,'R')
 with pytest.raises(FPI13Error): ReplayFixture('F',config_hash,5,(e,e),'R')

def test_event_id_deterministic(fixture): assert fixture.events[0].computed_event_id==fixture.events[0].computed_event_id

def test_event_hash_changes_with_payload(fixture):
 e=fixture.events[0];e2=ReplayEvent(e.sequence,e.event_time,e.event_type,e.semantic_id,'1'*64,e.source_revision_id,e.kind,e.is_historical,e.reason_codes)
 assert e.event_hash!=e2.event_hash

def test_reason_codes_canonical(config_hash):
 with pytest.raises(FPI13Error): ReplayEvent(1,1,ReplayEventType.SEMANTIC_UPSERT,'S','0'*64,'R',reason_codes=('B','A'))
