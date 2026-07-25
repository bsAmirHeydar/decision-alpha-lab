from dataclasses import replace
from fp_i04_data.golden import bar,golden_bars,golden_config,golden_pair
from fp_i04_data.synchronization import synchronize
from fp_i03_time.contracts import TimeKernelConfig

def test_transport_metadata_does_not_change_bar_semantics():
    a=bar('ES',60_000,5000,1)
    b=replace(a,source_id='OTHER',source_sequence=999,received_utc_ms=999999)
    assert a.bar_hash==b.bar_hash and a.bar_id==b.bar_id

def test_source_revision_changes_bar_semantics():
    a=bar('ES',60_000,5000,1,'R1');b=replace(a,source_revision='R2')
    assert a.bar_hash!=b.bar_hash

def test_price_change_changes_result_identity():
    start=1783900800000;bars=list(golden_bars(start,2));a=synchronize(golden_pair(),bars,start,start+120000,golden_config(),TimeKernelConfig())
    bars[0]=replace(bars[0],close=bars[0].close+.25,source_revision='R2')
    b=synchronize(golden_pair(),bars,start,start+120000,golden_config(),TimeKernelConfig())
    assert a.semantic_hash!=b.semantic_hash and a.result_id!=b.result_id

def test_transport_reordering_does_not_change_result_identity():
    start=1783900800000;bars=golden_bars(start,3)
    a=synchronize(golden_pair(),bars,start,start+180000,golden_config(),TimeKernelConfig())
    b=synchronize(golden_pair(),tuple(reversed(bars)),start,start+180000,golden_config(),TimeKernelConfig())
    assert a.result_id==b.result_id

def test_policy_change_changes_result_identity():
    start=1783900800000;bars=golden_bars(start,2);cfg=golden_config();a=synchronize(golden_pair(),bars,start,start+120000,cfg,TimeKernelConfig())
    b=synchronize(golden_pair(),bars,start,start+120000,replace(cfg,maximum_backfill_minutes=cfg.maximum_backfill_minutes-1),TimeKernelConfig())
    assert a.semantic_hash!=b.semantic_hash
