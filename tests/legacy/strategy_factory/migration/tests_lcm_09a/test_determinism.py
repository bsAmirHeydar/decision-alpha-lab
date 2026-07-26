from .conftest import j,jl
def test_registry_digests_are_stable():
 from src.engine.tooling.strategy_factory.lcm.lcm_09a.canonical import digest_object
 v=jl("variants/setup_variant_registry.jsonl"); assert all(digest_object(x,"variant_digest")==x["variant_digest"] for x in v)
 e=jl("embedded/embedded_setup_registry.jsonl"); assert all(digest_object(x,"candidate_digest")==x["candidate_digest"] for x in e)
def test_handoff_digest_is_stable():
 from src.engine.tooling.strategy_factory.lcm.lcm_09a.canonical import digest_object
 h=j("handoff/lcm09a_to_lcm09b_handoff.json"); assert digest_object(h,"handoff_digest")==h["handoff_digest"]
