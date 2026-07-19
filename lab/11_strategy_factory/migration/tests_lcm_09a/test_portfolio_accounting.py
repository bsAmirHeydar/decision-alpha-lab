from .conftest import j,jl
def test_all_setup_identities_accounted():
 inv=jl("inventory/setup_inventory.jsonl"); assert len(inv)==60; assert len({x["setup_id"] for x in inv})==60
def test_all_contracts_frozen_blocked():
 inv=jl("inventory/setup_inventory.jsonl"); assert {x["contract_status"] for x in inv}=={"FROZEN_BLOCKED_REFERENCE"}; assert not any(x["implementation_authorized"] for x in inv)
def test_source_hashes_verified():assert all(x["source_digest_verified"] for x in jl("inventory/setup_inventory.jsonl"))
