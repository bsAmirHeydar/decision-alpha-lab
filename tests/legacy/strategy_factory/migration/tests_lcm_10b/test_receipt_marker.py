from .conftest import j
from src.engine.tooling.strategy_factory.lcm.lcm_10b.canonical import digest_object
def test_receipt_and_marker_are_self_verifying():
 r=j("treatment_boundary_receipt.json");m=j("treatment_boundary_marker.json");assert r["receipt_digest"]==digest_object(r,"receipt_digest");assert m["marker_digest"]==digest_object(m,"marker_digest")
