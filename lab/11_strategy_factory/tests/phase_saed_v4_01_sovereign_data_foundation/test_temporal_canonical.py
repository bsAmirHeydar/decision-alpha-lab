import pytest
from saed_v4_data_foundation.canonical import canonical_json,content_hash,stable_id,merkle_root,normalize_time
from saed_v4_data_foundation.temporal import BitemporalStamp
from saed_v4_data_foundation.errors import TemporalIntegrityError

def test_canonical_order_independent(): assert canonical_json({'b':2,'a':1})==canonical_json({'a':1,'b':2})
def test_hash_order_independent(): assert content_hash({'b':2,'a':1})==content_hash({'a':1,'b':2})
def test_stable_id(): assert stable_id('x',{'a':1})==stable_id('x',{'a':1})
def test_merkle_order_independent(): assert merkle_root(['a','b'])==merkle_root(['b','a'])
def test_time_normalized(): assert normalize_time('2026-01-01T00:00:00+00:00').endswith('Z')
def test_bitemporal_valid(): assert BitemporalStamp('2026-01-01T00:00:00Z','2026-01-01T00:00:01Z').visible_as_of('2026-01-01T00:00:02Z')
def test_future_not_visible(): assert not BitemporalStamp('2026-01-01T00:00:00Z','2026-01-01T00:00:05Z').visible_as_of('2026-01-01T00:00:04Z')
def test_invalid_known_time():
 with pytest.raises(TemporalIntegrityError): BitemporalStamp('2026-01-01T00:00:02Z','2026-01-01T00:00:01Z')
def test_invalid_valid_to():
 with pytest.raises(TemporalIntegrityError): BitemporalStamp('2026-01-01T00:00:02Z','2026-01-01T00:00:03Z','2026-01-01T00:00:01Z')
