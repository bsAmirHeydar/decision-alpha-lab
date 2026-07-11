from pathlib import Path
import pytest
from strategy_factory_governance import *
from strategy_factory_governance.hashing import sha256_bytes

def test_inventory_is_order_independent_and_detects_duplicates(tmp_path):
    a=tmp_path/"a.bin";b=tmp_path/"b.json";a.write_bytes(b"model");b.write_text("{}",encoding="utf-8")
    da=digest_file(a,root=tmp_path,logical_name="model",role=ArtifactRole.MODEL,media_type="application/octet-stream")
    db=digest_file(b,root=tmp_path,logical_name="card",role=ArtifactRole.MODEL_CARD,media_type="application/json")
    assert inventory_hash([da,db])==inventory_hash([db,da])
    inv=build_inventory("test_inventory","1.0.0",[db,da],10);inv.validate();assert len(inv.inventory_hash)==64
    with pytest.raises(ValueError,match="duplicate artifact logical name"):
        validate_inventory([da,da])

def test_artifact_rejects_path_traversal():
    d=ArtifactDigest("x","../x",ArtifactRole.OTHER,"text/plain",1,"0"*64).with_id()
    with pytest.raises(ValueError,match="traversal-free"):d.validate()

def test_authenticity_is_distinct_from_integrity():
    from strategy_factory_governance.examples import reference_inventory
    inv=reference_inventory()
    unsigned=AuthenticityAttestation(AttestationKind.NONE,inv.inventory_hash,"","","","","",False,10).with_hash()
    validate_attestation(unsigned,inv.inventory_hash,require_verified=False)
    with pytest.raises(ValueError,match="verified authenticity"):
        validate_attestation(unsigned,inv.inventory_hash,require_verified=True)
