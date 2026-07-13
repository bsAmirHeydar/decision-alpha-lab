from dataclasses import replace
from fp_i04_data.enums import RevisionKind
from fp_i04_data.golden import golden_bars,golden_config,golden_pair,bar
from fp_i04_data.revision import classify_revision,revision_impact
from fp_i04_data.synchronization import synchronize
from fp_i03_time.contracts import TimeKernelConfig

def test_initial_revision():
    start=1783900800000;r=classify_revision('FP-PAIR-ES-NQ',golden_bars(start,2))
    assert r.kind is RevisionKind.INITIAL

def test_append_revision():
    start=1783900800000;old=golden_bars(start,2);new=old+(bar('ES',start+120000,5002,4),bar('NQ',start+120000,20002,5))
    assert classify_revision('FP-PAIR-ES-NQ',new,old,'P').kind is RevisionKind.APPEND

def test_late_insert_revision():
    start=1783900800000;full=golden_bars(start,3);old=tuple(b for b in full if not(b.canonical_symbol=='ES' and b.open_utc_ms==start+60000))
    assert classify_revision('FP-PAIR-ES-NQ',full,old,'P').kind is RevisionKind.LATE_INSERT

def test_value_correction_revision():
    start=1783900800000;old=golden_bars(start,2);new=list(old);new[0]=replace(new[0],close=new[0].close+.25,source_revision='R2')
    assert classify_revision('FP-PAIR-ES-NQ',new,old,'P').kind is RevisionKind.VALUE_CORRECTION

def test_delete_revision():
    start=1783900800000;old=golden_bars(start,2);new=old[:-1]
    assert classify_revision('FP-PAIR-ES-NQ',new,old,'P').kind is RevisionKind.DELETE

def test_no_change_revision():
    start=1783900800000;old=golden_bars(start,2)
    assert classify_revision('FP-PAIR-ES-NQ',old,old,'P').kind is RevisionKind.NO_CHANGE

def test_revision_impact_preserves_prefix_hash():
    start=1783900800000;old=golden_bars(start,4);new=list(old);new[-2]=replace(new[-2],close=new[-2].close+.25,source_revision='R2')
    r=synchronize(golden_pair(),new,start,start+240000,golden_config(),TimeKernelConfig(),old,parent_revision_id='P')
    impact=revision_impact(r.revision,r.rows,('W1','W2'))
    assert impact.affected_minute_ids==(start+180000,) and impact.affected_window_ids==('W1','W2')
