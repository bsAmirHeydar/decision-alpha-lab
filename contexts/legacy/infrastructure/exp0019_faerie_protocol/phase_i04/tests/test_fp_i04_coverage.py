from fp_i04_data.coverage import coverage_interval,gaps_for_axis
from fp_i04_data.enums import CoverageState,GapReason
from fp_i04_data.golden import bar

def test_complete_coverage():
    bars=tuple(bar('ES',i*60_000,5000+i) for i in range(3))
    c=coverage_interval('ES',0,180_000,bars,(0,60_000,120_000))
    assert c.state is CoverageState.COMPLETE and c.coverage_ratio==1

def test_partial_coverage():
    bars=(bar('ES',0,5000),bar('ES',120_000,5002))
    c=coverage_interval('ES',0,180_000,bars,(0,60_000,120_000))
    assert c.state is CoverageState.PARTIAL and c.present_minutes==2

def test_calendar_excluded_minutes_are_not_missing():
    bars=(bar('ES',0,5000),)
    c=coverage_interval('ES',0,180_000,bars,(0,))
    assert c.expected_minutes==1 and c.calendar_excluded_minutes==2 and c.state is CoverageState.COMPLETE

def test_gap_reason_distinguishes_before_inside_after():
    bars=(bar('ES',60_000,5001),bar('ES',180_000,5003))
    gaps=gaps_for_axis('ES',(0,60_000,120_000,180_000,240_000),bars,'R')
    assert [g.reason for g in gaps]==[GapReason.BEFORE_COVERAGE,GapReason.SOURCE_MISSING,GapReason.AFTER_COVERAGE]

def test_conflict_gap_reason_is_explicit():
    gaps=gaps_for_axis('ES',(60_000,),(), 'R',(60_000,))
    assert gaps[0].reason is GapReason.DUPLICATE_CONFLICT
