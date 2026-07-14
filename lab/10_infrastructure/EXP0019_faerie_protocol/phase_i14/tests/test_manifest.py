import pytest
from fp_i14_diagnostic import *
def test_manifest_ids_differ_by_product(manifests): assert len({m.computed_manifest_id for m in manifests.values()})==3
def test_semantic_manifest_same(manifests): assert len({m.semantic_manifest_hash for m in manifests.values()})==1
def test_module_versions_exact(manifests): assert all(len(m.module_versions)==11 for m in manifests.values())
def test_host_tf_required(config_hash):
    with pytest.raises(FPI14Error): build_manifest(ProductKind.INDICATOR,config_hash,host_tf=0)
