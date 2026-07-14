from dataclasses import replace
from fp_i14_diagnostic import *
def test_checkpoint_accepts(runs):
    r=runs[ProductKind.INDICATOR];cp=create_checkpoint(r);assert validate_checkpoint(cp,r.manifest,r.fixture_id).disposition==CheckpointDisposition.ACCEPTED
def test_checkpoint_config_rejects(runs):
    r=runs[ProductKind.INDICATOR];cp=create_checkpoint(r);m=build_manifest(ProductKind.INDICATOR,sha256('other'));assert validate_checkpoint(cp,m,r.fixture_id).disposition==CheckpointDisposition.REJECT_CONFIG
def test_checkpoint_product_rejects(runs):
    r=runs[ProductKind.INDICATOR];cp=create_checkpoint(r);m=build_manifest(ProductKind.DIAGNOSTIC_EA,r.manifest.config_hash);assert validate_checkpoint(cp,m,r.fixture_id).disposition==CheckpointDisposition.REJECT_PRODUCT
def test_checkpoint_hash_rejects(runs):
    r=runs[ProductKind.INDICATOR];cp=replace(create_checkpoint(r),payload_hash='0'*64);assert validate_checkpoint(cp,r.manifest,r.fixture_id).disposition==CheckpointDisposition.REJECT_HASH
