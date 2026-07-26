from .conftest import ROOT,j
def contracts():return [j("setup_contracts/"+p.name) for p in sorted((ROOT/"setup_contracts").glob("*.json"))]
def test_contract_count_and_digests():
 from src.engine.tooling.strategy_factory.lcm.lcm_09a.canonical import digest_object
 c=contracts(); assert len(c)==60; assert all(digest_object(x,"contract_digest")==x["contract_digest"] for x in c)
def test_no_broker_drawing_or_quota_semantics_embedded():
 for c in contracts():
  a=c["authority_boundary"]; assert not a["broker_state_in_canonical_contract"]; assert not a["drawing_state_in_canonical_contract"]; assert not a["execution_quota_in_canonical_contract"]
def test_no_trade_and_unknown_are_first_class():
 assert all(c["abstention_contract"]["no_trade_is_first_class"] and c["unknown_policy"]["mandatory_unknowns_block_implementation"] for c in contracts())
