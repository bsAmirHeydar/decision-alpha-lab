from strategy_factory_dataset_v3.golden import *
from strategy_factory_dataset_v3.splits import build_purged_embargoed_plan
from strategy_factory_dataset_v3.leakage import audit_dataset

def test_clean_leakage_report_not_blocked():
 anchors=golden_anchors(8); p=build_purged_embargoed_plan(anchors,fold_count=3); r=audit_dataset(dataset_id='ds',anchors=anchors,rows=(),split_plan=p,transform_plans=(),rebuild_hash_a='a',rebuild_hash_b='a'); assert not r.blocked

def test_rebuild_mismatch_blocks():
 anchors=golden_anchors(8); p=build_purged_embargoed_plan(anchors,fold_count=3); r=audit_dataset(dataset_id='ds',anchors=anchors,rows=(),split_plan=p,transform_plans=(),rebuild_hash_a='a',rebuild_hash_b='b'); assert r.blocked; assert any(x.code=='non_reproducible_dataset' for x in r.findings)

def test_future_perturbation_blocks():
 anchors=golden_anchors(8); p=build_purged_embargoed_plan(anchors,fold_count=3); r=audit_dataset(dataset_id='ds',anchors=anchors,rows=(),split_plan=p,transform_plans=(),rebuild_hash_a='a',rebuild_hash_b='a',future_perturbation_passed=False); assert r.blocked
