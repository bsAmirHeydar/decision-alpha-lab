from decimal import Decimal as D
from collections import defaultdict
from strategy_factory_dataset_v3.golden import golden_anchors
from strategy_factory_dataset_v3.splits import build_purged_embargoed_plan
from strategy_factory_dataset_v3.transforms import fit_transform_plan
from strategy_factory_dataset_v3.enums import FoldRole

def test_cluster_never_crosses_train_test():
 p=build_purged_embargoed_plan(golden_anchors(8),fold_count=3,purge_ms=1,embargo_ms=1); d=defaultdict(lambda:defaultdict(set))
 for a in p.assignments:d[a.fold_id][a.dependence_cluster_id].add(a.role)
 assert all(not ({FoldRole.TRAIN,FoldRole.TEST}<=roles) for clusters in d.values() for roles in clusters.values())

def test_siblings_lock_by_opportunity():
 p=build_purged_embargoed_plan(golden_anchors(8),fold_count=3); assert p.sibling_lock

def test_transform_fit_rows_are_train_only():
 anchors=golden_anchors(8); p=build_purged_embargoed_plan(anchors,fold_count=3); feats={a.opportunity_id:{'x':D(i),'y':None if i%2 else D(i*2)} for i,a in enumerate(anchors)}; fold=next(f.fold_id for f in p.folds if any(a.fold_id==f.fold_id and a.role==FoldRole.TRAIN for a in p.assignments)); t=fit_transform_plan(transform_id='transform.reference',version='1.0.0',fold_id=fold,feature_rows=feats,split_plan=p); roles={(a.fold_id,a.opportunity_id):a.role for a in p.assignments}; assert all(roles[(fold,oid)]==FoldRole.TRAIN for oid in t.fit_opportunity_ids)
