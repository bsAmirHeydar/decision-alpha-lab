import pytest
from fp_i03_time.contracts import TimeKernelConfig
from fp_i04_data.cursor import advance_cursor,empty_cursor,validate_resume
from fp_i04_data.enums import CursorState
from fp_i04_data.errors import FPI04Error
from fp_i04_data.golden import golden_bars,golden_config,golden_pair
from fp_i04_data.synchronization import synchronize

def test_empty_cursor():
    c=empty_cursor('FP-PAIR-ES-NQ');assert c.state is CursorState.EMPTY and c.last_emitted_open_utc_ms is None

def test_advance_cursor_records_sequences_and_revision():
    start=1783900800000;r=synchronize(golden_pair(),golden_bars(start,2),start,start+120000,golden_config(),TimeKernelConfig())
    c=advance_cursor(empty_cursor(r.pair_id),r)
    assert c.last_emitted_open_utc_ms==start+60000 and c.data_revision_id==r.revision.revision_id and c.right_last_source_sequence==3

def test_resume_accepts_matching_parent():
    start=1783900800000;r=synchronize(golden_pair(),golden_bars(start,1),start,start+60000,golden_config(),TimeKernelConfig())
    c=advance_cursor(empty_cursor(r.pair_id),r);assert validate_resume(c,r.revision.revision_id)

def test_resume_rejects_revision_mismatch():
    start=1783900800000;r=synchronize(golden_pair(),golden_bars(start,1),start,start+60000,golden_config(),TimeKernelConfig())
    c=advance_cursor(empty_cursor(r.pair_id),r)
    with pytest.raises(FPI04Error,match='differs'):validate_resume(c,'OTHER')
