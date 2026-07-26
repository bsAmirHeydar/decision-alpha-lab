from src.engine.tooling.strategy_factory.lcm.lcm_09b.canonical import digest_object
from .conftest import j,jl
def test_registry_and_handoff_digests_are_stable():
 r=j("canonical_setup_registry.json");h=j("handoff/lcm09b_to_lcm10a_handoff.json");assert digest_object(r,"registry_digest")==r["registry_digest"];assert digest_object(h,"handoff_digest")==h["handoff_digest"]
def test_jsonl_order_is_deterministic():
 for rel,key in (("parity/setup_parity_registry.jsonl","setup_id"),("dependencies/treatment_dependency_inventory_seed.jsonl","setup_id")):
  rows=jl(rel);assert [x[key] for x in rows]==sorted(x[key] for x in rows)
