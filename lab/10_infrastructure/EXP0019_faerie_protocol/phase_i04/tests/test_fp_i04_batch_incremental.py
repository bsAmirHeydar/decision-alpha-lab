from fp_i03_time.contracts import TimeKernelConfig
from fp_i04_data.golden import golden_bars,golden_config,golden_pair
from fp_i04_data.synchronization import synchronize

def test_batch_and_chunked_row_sequence_match():
    start=1783900800000;bars=golden_bars(start,6);pair=golden_pair();cfg=golden_config();tc=TimeKernelConfig()
    batch=synchronize(pair,bars,start,start+360000,cfg,tc)
    first=synchronize(pair,tuple(b for b in bars if b.open_utc_ms<start+180000),start,start+180000,cfg,tc)
    second=synchronize(pair,tuple(b for b in bars if b.open_utc_ms>=start+180000),start+180000,start+360000,cfg,tc)
    assert tuple(r.open_utc_ms for r in batch.rows)==tuple(r.open_utc_ms for r in first.rows+second.rows)
    assert tuple((r.left.bar.bar_hash,r.right.bar.bar_hash) for r in batch.rows)==tuple((r.left.bar.bar_hash,r.right.bar.bar_hash) for r in first.rows+second.rows)

def test_chunk_boundary_has_no_duplicate_minute():
    start=1783900800000;bars=golden_bars(start,4);pair=golden_pair();cfg=golden_config();tc=TimeKernelConfig()
    one=synchronize(pair,tuple(b for b in bars if b.open_utc_ms<start+120000),start,start+120000,cfg,tc)
    two=synchronize(pair,tuple(b for b in bars if b.open_utc_ms>=start+120000),start+120000,start+240000,cfg,tc)
    ids=[r.open_utc_ms for r in one.rows+two.rows];assert len(ids)==len(set(ids))==4
