from fp_i13_release import *
def facts():return tuple(ProjectionFact(f'O{i}',f'S{i}',ObjectPriority.CRITICAL if i<2 else (ObjectPriority.HISTORICAL if i>7 else ObjectPriority.NORMAL),i>7,True) for i in range(10))
def test_no_degradation_under_budget():assert apply_projection_budget(facts(),20).health==HealthState.READY
def test_degradation_defers_noncritical():
 d=apply_projection_budget(facts(),5);assert d.health==HealthState.DEGRADED and len(d.deferred_object_ids)==5
def test_critical_objects_preserved():
 d=apply_projection_budget(facts(),2);assert set(d.projected_object_ids)=={'O0','O1'}
def test_semantic_count_never_reduced():assert apply_projection_budget(facts(),3).semantic_count==10
