from fp_i12_operator import *
def test_benchmark(snapshot,config):
 r=benchmark(snapshot.items,snapshot,config,50);assert r['per_loop_ms']<20
def test_large_filter_linear(snapshot,config):
 items=tuple(snapshot.items)*1000;r=apply_filters(items,config.filters,snapshot.computed_hash);assert len(r.included)==4000
