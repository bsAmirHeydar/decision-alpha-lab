from __future__ import annotations
from strategy_factory_contexts_v3 import *
from strategy_factory_contexts_v3.fixtures import synthetic_records, exp0017_records

def test_synthetic_long_short_and_abstention():
    p=SyntheticBreakContextPackage(); rows=synthetic_records()
    assert p.observe(rows[0])[0].payload["direction"]=="long"
    assert p.observe(rows[1])==()
    assert p.observe(rows[2])[0].payload["direction"]=="short"

def test_exp0017_reference_consumes_adapter_record():
    p=EXP0017ContextPackage(); o=p.observe(exp0017_records()[0])[0]; f=p.build_feature_frame(o,{})
    values={x.feature_id:x.value for x in f.values}
    assert values["exp0017.direction"]=="short"
    assert values["exp0017.group_minutes"]==60
    assert values["exp0017.hunter_displacement"]==25.0
    assert values["exp0017.clean_displacement"]==1.0
    assert values["exp0017.divergence_gap"]==24.0

def test_reference_packages_have_manual_baseline_and_task():
    for p in (SyntheticBreakContextPackage(),EXP0017ContextPackage()):
        assert p.manifest.manual_policies
        assert p.manifest.tasks
        assert p.manifest.tasks[0].allowed_view_ids
        assert p.manifest.feature_packs and p.manifest.cluster_rules
