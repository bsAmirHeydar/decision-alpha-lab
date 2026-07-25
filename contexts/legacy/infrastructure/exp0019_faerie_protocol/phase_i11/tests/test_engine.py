from fp_i11_visual import *

def test_engine_initial_projection(snapshot,cfg,layout):
 e=VisualProjectionEngine(cfg);r=e.project(snapshot,layout);assert r.object_count>0 and len(r.dirty_set.creates)>0
def test_engine_second_projection_unchanged(snapshot,cfg,layout):
 e=VisualProjectionEngine(cfg);e.project(snapshot,layout);r=e.project(snapshot,layout);assert len(r.dirty_set.unchanged)==r.object_count
def test_projection_deterministic(snapshot,cfg,layout):
 e1=VisualProjectionEngine(cfg);e2=VisualProjectionEngine(cfg);assert e1.project(snapshot,layout).projection_hash==e2.project(snapshot,layout).projection_hash
def test_object_budget_degrades(snapshot,layout):
 cfg=ProjectionConfig('I','FP19::I::',max_objects=100);e=VisualProjectionEngine(cfg);r=e.project(snapshot,layout);assert r.object_count<=100
