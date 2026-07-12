from decimal import Decimal as D
from strategy_factory_dataset_v3.golden import *
from strategy_factory_dataset_v3.splits import build_purged_embargoed_plan
from strategy_factory_dataset_v3.dataset import DatasetBuilder

def test_end_to_end_dataset_build_is_immutable_and_accepted():
 anchors=golden_anchors(8); split=build_purged_embargoed_plan(anchors,fold_count=3)
 kwargs=dict(dataset_id='dataset.reference',version='1.0.0',context_package_key='context.synthetic@1.0.0',anchors=anchors,treatments_by_opportunity={a.opportunity_id:golden_treatments(a) for a in anchors},paths_by_opportunity={a.opportunity_id:golden_path(a) for a in anchors},scenarios=golden_scenarios(),horizons_ms=[300000],tasks=golden_tasks(),split_plan=split,transform_plans=(),feature_values_by_opportunity={a.opportunity_id:{'x':D(i)} for i,a in enumerate(anchors)})
 a=DatasetBuilder().build(**kwargs); b=DatasetBuilder().build(**kwargs); assert a.manifest.manifest_hash==b.manifest.manifest_hash; assert a.build_report.accepted; assert a.manifest.row_count==len(a.rows)

def test_treatment_siblings_have_distinct_rows_but_common_opportunity():
 anchors=golden_anchors(8); split=build_purged_embargoed_plan(anchors,fold_count=3); d=DatasetBuilder().build(dataset_id='dataset.reference',version='1.0.0',context_package_key='context.synthetic@1.0.0',anchors=anchors,treatments_by_opportunity={a.opportunity_id:golden_treatments(a) for a in anchors},paths_by_opportunity={a.opportunity_id:golden_path(a) for a in anchors},scenarios=golden_scenarios(),horizons_ms=[300000],tasks=golden_tasks()[:1],split_plan=split,transform_plans=(),feature_values_by_opportunity={}); first=anchors[0].opportunity_id; rows=[r for r in d.rows if r.opportunity_id==first]; assert len({r.treatment_id for r in rows})==2; assert len({tuple(sorted(r.fold_roles.items())) for r in rows})==1
