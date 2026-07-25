from .conftest import j
def test_handoff_and_receipt_create_no_authority():
 h=j("handoff/lcm09b_to_lcm10a_handoff.json");r=j("setup_migration_receipt.json")
 for k in ("consumer_cutover_allowed","promotion_authority_created","runtime_authority_created","live_order_authority_created","capital_authority_created"):assert h[k] is False
 assert r["consumer_cutover_performed"] is False and r["source_move_performed"] is False and r["source_delete_performed"] is False
