from dataclasses import replace
from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import *

def test_clean_dataset_audit_is_deterministic():
    bundle=build_reference_training_bundle()[0]
    a=audit_dataset(bundle.manifest,bundle.rows,len(bundle.columns));b=audit_dataset(bundle.manifest,bundle.rows,len(bundle.columns))
    assert a.fatal_count==0 and a.audit_hash==b.audit_hash

def test_duplicate_row_is_fatal():
    bundle=build_reference_training_bundle()[0]
    report=audit_dataset(replace(bundle.manifest,row_count=bundle.manifest.row_count+1,dataset_hash=""),bundle.rows+(bundle.rows[0],),len(bundle.columns))
    assert report.fatal_count>=1
