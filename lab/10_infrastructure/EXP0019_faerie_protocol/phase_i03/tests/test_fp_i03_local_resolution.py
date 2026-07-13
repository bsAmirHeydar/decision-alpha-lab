from datetime import datetime
import pytest
from fp_i03_time.enums import LocalResolutionPolicy, LocalTimeStatus
from fp_i03_time.errors import FPI03Error
from fp_i03_time.time_math import local_candidates_utc_ms, require_resolved_local, resolve_local, utc_to_new_york


def test_unique_local_time_roundtrips():
    local=datetime(2026,7,13,9,30)
    result=resolve_local(local,LocalResolutionPolicy.REJECT)
    assert result.status is LocalTimeStatus.UNIQUE
    assert len(result.candidate_utc_ms)==1
    assert utc_to_new_york(result.selected_utc_ms).local_iso.startswith("2026-07-13T09:30:00")

@pytest.mark.parametrize("policy,index",[(LocalResolutionPolicy.EARLIEST,0),(LocalResolutionPolicy.LATEST,1)])
def test_ambiguous_fall_time_policy(policy,index):
    local=datetime(2026,11,1,1,30)
    result=resolve_local(local,policy)
    assert result.status is LocalTimeStatus.AMBIGUOUS
    assert len(result.candidate_utc_ms)==2
    assert result.selected_utc_ms==result.candidate_utc_ms[index]
    assert utc_to_new_york(result.candidate_utc_ms[0]).fold==0
    assert utc_to_new_york(result.candidate_utc_ms[1]).fold==1


def test_ambiguous_reject_has_no_selection():
    result=resolve_local(datetime(2026,11,1,1,30),LocalResolutionPolicy.REJECT)
    assert result.status is LocalTimeStatus.AMBIGUOUS
    assert result.selected_utc_ms is None


def test_nonexistent_spring_time_has_no_candidates():
    result=resolve_local(datetime(2026,3,8,2,30),LocalResolutionPolicy.EARLIEST)
    assert result.status is LocalTimeStatus.NONEXISTENT
    assert result.candidate_utc_ms==()
    assert result.selected_utc_ms is None


def test_require_resolved_raises_for_nonexistent():
    with pytest.raises(FPI03Error) as exc:
        require_resolved_local(datetime(2026,3,8,2,30),LocalResolutionPolicy.REJECT)
    assert exc.value.code=="FP_TRC_LOCAL_NONEXISTENT"


def test_aware_local_input_is_rejected():
    from datetime import timezone
    with pytest.raises(FPI03Error) as exc:
        local_candidates_utc_ms(datetime(2026,7,1,tzinfo=timezone.utc))
    assert exc.value.code=="FP_TRC_LOCAL_AWARE"
