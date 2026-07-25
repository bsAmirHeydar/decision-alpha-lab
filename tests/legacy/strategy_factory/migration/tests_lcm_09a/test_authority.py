from .conftest import j,jl
def test_handoff_has_zero_execution_authority():
 h=j("handoff/lcm09a_to_lcm09b_handoff.json"); assert h["implementation_authorized_setup_ids"]==[]
 for k in ("consumer_cutover_allowed","source_move_allowed","source_delete_allowed","runtime_authority_created","live_order_authority_created","capital_authority_created"): assert not h[k]
def test_inventory_has_no_cutover_or_authority():
 assert all(not x["consumer_cutover_authorized"] and not x["runtime_authority_created"] and not x["live_order_authority_created"] and not x["capital_authority_created"] for x in jl("inventory/setup_inventory.jsonl"))
