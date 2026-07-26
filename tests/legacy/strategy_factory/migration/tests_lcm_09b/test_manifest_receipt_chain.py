from src.engine.tooling.strategy_factory.lcm.lcm_09b.canonical import digest_object
from .conftest import j

def test_receipt_binds_manifest_and_handoff_without_digest_cycle():
 m=j("output_manifest.json"); r=j("setup_migration_receipt.json"); h=j("handoff/lcm09b_to_lcm10a_handoff.json")
 assert digest_object(r,"receipt_digest")==r["receipt_digest"]
 assert r["output_manifest_digest"]==m["manifest_digest"]
 assert r["handoff_digest"]==h["handoff_digest"]
 assert all(x["path"] not in {"output_manifest.json","setup_migration_receipt.json"} for x in m["files"])
