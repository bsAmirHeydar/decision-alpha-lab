from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import *

def test_reference_dataset_is_reproducible():
    a=build_reference_training_bundle()[0];b=build_reference_training_bundle()[0]
    assert a.manifest.dataset_hash==b.manifest.dataset_hash and a.manifest.row_count==24
    assert (a.manifest.train_count,a.manifest.validation_count,a.manifest.test_count)==(12,6,6)

def test_cluster_cannot_cross_roles():
    c=(FeatureColumn("f","1",0).with_hash(),);l=LabelContract("l","1",LabelKind.BINARY_NET_R).with_hash()
    obs=[SourceObservation("fold",DatasetRole.TRAIN,"e1","cluster","c1","o1","s1",1,2,3,{"f":1},1),
         SourceObservation("fold",DatasetRole.TEST,"e2","cluster","c2","o2","s2",4,5,6,{"f":2},1)]
    try:build_dataset(dataset_id="d",dataset_version="1",strategy_id="s",source_run_id="r",source_manifest_hash="m",source_artifact_hash="a",validation_plan_hash="v",columns=c,label_contract=l,observations=obs,created_at_utc_msc=1,code_revision="x");assert False
    except ValueError as error:assert "cluster" in str(error)

def test_future_feature_time_rejected():
    bundle=build_reference_training_bundle()[0];row=bundle.rows[0]
    from dataclasses import replace
    bad=replace(row,known_time_utc_msc=row.decision_time_utc_msc+1,row_id="",row_hash="").with_hashes()
    try:bad.validate(len(bundle.columns));assert False
    except ValueError as error:assert "causality" in str(error)
