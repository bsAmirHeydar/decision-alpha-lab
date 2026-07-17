from pathlib import Path
import pytest
from tools.strategy_factory.acl_os.acl_05.canonical import digest_bytes
from tools.strategy_factory.acl_os.acl_05.event_ledger import EventLedger, verify_event_ledger
from tools.strategy_factory.acl_os.acl_05.object_store import ContentAddressedStore

def test_store_uses_exact_byte_digest(tmp_path):
    s=ContentAddressedStore(tmp_path,10,1000); r=s.put(logical_id="TEST_OBJECT",artifact_class="TEST",media_type="text/plain",payload=b"abc",semantic_digest=None,source_path="test"); assert r["blob_digest"]==digest_bytes(b"abc")

def test_store_path_shape(tmp_path):
    s=ContentAddressedStore(tmp_path,10,1000); r=s.put(logical_id="TEST_OBJECT",artifact_class="TEST",media_type="text/plain",payload=b"abc",semantic_digest=None,source_path="test"); assert r["store_path"].startswith("objects/sha256/") and r["store_path"].endswith(".blob")

def test_duplicate_bytes_deduplicate(tmp_path):
    s=ContentAddressedStore(tmp_path,10,1000); s.put(logical_id="OBJECT_A",artifact_class="TEST",media_type="text/plain",payload=b"abc",semantic_digest=None,source_path="a"); s.put(logical_id="OBJECT_B",artifact_class="TEST",media_type="text/plain",payload=b"abc",semantic_digest=None,source_path="b"); idx=s.index(); assert idx["object_count"]==1 and idx["reference_count"]==2

def test_object_budget_enforced(tmp_path):
    s=ContentAddressedStore(tmp_path,1,1000); s.put(logical_id="OBJECT_A",artifact_class="TEST",media_type="text/plain",payload=b"a",semantic_digest=None,source_path="a")
    with pytest.raises(Exception): s.put(logical_id="OBJECT_B",artifact_class="TEST",media_type="text/plain",payload=b"b",semantic_digest=None,source_path="b")

def test_byte_budget_enforced(tmp_path):
    s=ContentAddressedStore(tmp_path,10,2)
    with pytest.raises(Exception): s.put(logical_id="OBJECT_A",artifact_class="TEST",media_type="text/plain",payload=b"abc",semantic_digest=None,source_path="a")

def test_ledger_hash_chain_valid():
    l=EventLedger("BATCH_SEED"); l.append("ONE",{},"2026-07-18T00:00:00Z"); l.append("TWO",{},"2026-07-18T00:00:00Z"); assert verify_event_ledger(l.document())

def test_ledger_tamper_detected():
    l=EventLedger("BATCH_SEED"); l.append("ONE",{},"2026-07-18T00:00:00Z"); d=l.document(); d["events"][0]["payload"]={"tampered":True}; assert not verify_event_ledger(d)

def test_store_objects_are_read_only(tmp_path):
    s=ContentAddressedStore(tmp_path,10,1000); r=s.put(logical_id="OBJECT_A",artifact_class="TEST",media_type="text/plain",payload=b"abc",semantic_digest=None,source_path="a"); mode=(tmp_path/r["store_path"]).stat().st_mode; assert mode & 0o222 == 0
