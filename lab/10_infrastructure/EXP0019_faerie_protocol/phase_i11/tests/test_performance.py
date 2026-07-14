from fp_i11_visual import *

def test_dirty_set_avoids_recreate(snapshot,cfg,layout):
 e=VisualProjectionEngine(cfg);e.project(snapshot,layout);b=benchmark(e,snapshot,layout,10);assert b['unchanged']==b['object_count']
def test_benchmark_has_time(snapshot,cfg,layout): assert benchmark(VisualProjectionEngine(cfg),snapshot,layout,2)['total_us']>=0
