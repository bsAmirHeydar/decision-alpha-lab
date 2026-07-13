from dataclasses import replace
from fp_i03_time.contracts import TimeKernelConfig
from fp_i04_data.enums import MinuteCellState,SynchronizationHealth
from fp_i04_data.golden import bar,golden_bars,golden_config,golden_pair
from fp_i04_data.synchronization import synchronize,snapshot_from_result

def test_complete_pair_is_ready():
    start=1783900800000;r=synchronize(golden_pair(),golden_bars(start,4),start,start+240000,golden_config(),TimeKernelConfig())
    assert r.health is SynchronizationHealth.READY and r.both_present_minutes==4

def test_missing_inside_coverage_is_degraded():
    start=1783900800000;bars=list(golden_bars(start,4));bars=[b for b in bars if not(b.canonical_symbol=='NQ' and b.open_utc_ms==start+120000)]
    r=synchronize(golden_pair(),bars,start,start+240000,golden_config(),TimeKernelConfig())
    assert r.health is SynchronizationHealth.DEGRADED
    row=next(x for x in r.rows if x.open_utc_ms==start+120000)
    assert row.right.state is MinuteCellState.MISSING

def test_before_and_after_source_are_out_of_coverage():
    start=1783900800000;bars=(bar('ES',start+60000,5000),bar('NQ',start+60000,20000))
    r=synchronize(golden_pair(),bars,start,start+180000,golden_config(),TimeKernelConfig())
    assert r.rows[0].left.state is MinuteCellState.OUT_OF_COVERAGE and r.rows[-1].right.state is MinuteCellState.OUT_OF_COVERAGE

def test_conflicting_duplicate_blocks_result():
    start=1783900800000;bars=list(golden_bars(start,2));bars.append(bar('ES',start,9999,99))
    r=synchronize(golden_pair(),bars,start,start+120000,golden_config(),TimeKernelConfig())
    assert r.health is SynchronizationHealth.BLOCKED and r.rows[0].left.state is MinuteCellState.CONFLICT

def test_repeated_input_is_byte_semantic_equivalent():
    start=1783900800000;args=(golden_pair(),golden_bars(start,3),start,start+180000,golden_config(),TimeKernelConfig())
    assert synchronize(*args)==synchronize(*args)

def test_input_order_is_irrelevant():
    start=1783900800000;bars=golden_bars(start,3)
    assert synchronize(golden_pair(),bars,start,start+180000,golden_config(),TimeKernelConfig()).semantic_hash==synchronize(golden_pair(),tuple(reversed(bars)),start,start+180000,golden_config(),TimeKernelConfig()).semantic_hash

def test_snapshot_carries_exact_revision():
    start=1783900800000;r=synchronize(golden_pair(),golden_bars(start,2),start,start+120000,golden_config(),TimeKernelConfig())
    s=snapshot_from_result(r,start+999999)
    assert s.data_revision_id==r.revision.revision_id and len(s.row_ids)==2

def test_value_correction_marks_cell_revised():
    start=1783900800000;old=golden_bars(start,2);new=list(old);new[0]=replace(new[0],close=new[0].close+0.25,source_revision='R2')
    r=synchronize(golden_pair(),new,start,start+120000,golden_config(),TimeKernelConfig(),old,parent_revision_id='P')
    assert r.rows[0].left.state is MinuteCellState.REVISED
