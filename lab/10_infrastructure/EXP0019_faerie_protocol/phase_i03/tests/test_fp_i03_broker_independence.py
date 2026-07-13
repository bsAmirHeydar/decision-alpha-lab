import pytest
from fp_i03_time.broker import snapshot_from_broker
from fp_i03_time.contracts import BrokerTimestamp
from fp_i03_time.errors import FPI03Error
from fp_i03_time.golden import utc_ms


def test_two_broker_clocks_resolve_same_utc_and_same_identity():
    utc=utc_ms("2026-07-13T13:30:00Z")
    broker_plus2=utc+120*60_000
    broker_plus3=utc+180*60_000
    a=snapshot_from_broker(broker_plus2,120)
    b=snapshot_from_broker(broker_plus3,180)
    assert a.reference_utc_ms==b.reference_utc_ms==utc
    assert a.snapshot_id==b.snapshot_id
    assert a.ny_timestamp.timestamp_id==b.ny_timestamp.timestamp_id

@pytest.mark.parametrize("offset",[-841,841])
def test_invalid_broker_offset_rejected(offset):
    with pytest.raises(FPI03Error) as exc:
        BrokerTimestamp(1000,offset)
    assert exc.value.code=="FP_TRC_BROKER_OFFSET_INVALID"
