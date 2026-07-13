from datetime import datetime, timedelta, timezone
import pytest
from zoneinfo import ZoneInfo

from fp_i03_time.enums import DstRegime
from fp_i03_time.errors import FPI03Error
from fp_i03_time.time_math import dst_end_utc, dst_start_utc, is_dst_utc, utc_to_new_york

UTC=timezone.utc

@pytest.mark.parametrize("year,start,end", [
    (2007,"2007-03-11T07:00:00+00:00","2007-11-04T06:00:00+00:00"),
    (2020,"2020-03-08T07:00:00+00:00","2020-11-01T06:00:00+00:00"),
    (2026,"2026-03-08T07:00:00+00:00","2026-11-01T06:00:00+00:00"),
    (2035,"2035-03-11T07:00:00+00:00","2035-11-04T06:00:00+00:00"),
])
def test_dst_transition_instants(year,start,end):
    assert dst_start_utc(year).isoformat()==start
    assert dst_end_utc(year).isoformat()==end

@pytest.mark.parametrize("iso,expected", [
    ("2026-03-08T06:59:59+00:00",False),
    ("2026-03-08T07:00:00+00:00",True),
    ("2026-11-01T05:59:59+00:00",True),
    ("2026-11-01T06:00:00+00:00",False),
])
def test_dst_half_open_boundary(iso,expected):
    assert is_dst_utc(datetime.fromisoformat(iso)) is expected

@pytest.mark.parametrize("iso", [
    "2007-01-15T12:00:00+00:00","2007-07-15T12:00:00+00:00",
    "2026-03-08T06:59:59+00:00","2026-03-08T07:00:00+00:00",
    "2026-11-01T05:59:59+00:00","2026-11-01T06:00:00+00:00",
    "2035-12-15T12:00:00+00:00",
])
def test_utc_to_ny_matches_zoneinfo(iso):
    point=datetime.fromisoformat(iso)
    ours=utc_to_new_york(point)
    theirs=point.astimezone(ZoneInfo("America/New_York"))
    assert ours.utc_offset_minutes==int(theirs.utcoffset().total_seconds()//60)
    assert ours.local_iso[:19]==theirs.replace(tzinfo=None).isoformat(timespec="seconds")


def test_unsupported_year_fails_closed():
    with pytest.raises(FPI03Error) as exc:
        dst_start_utc(2006)
    assert exc.value.code=="FP_TRC_YEAR_UNSUPPORTED"
