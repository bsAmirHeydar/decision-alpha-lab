from .conftest import jl
def test_unknown_queue_is_open_and_blocking():
 rows=jl("unknowns/setup_unknown_queue.jsonl"); assert rows; assert all(x["blocking"] and x["resolution_state"]=="OPEN" for x in rows)
def test_each_setup_has_unknown_record():
 inv=jl("inventory/setup_inventory.jsonl"); q=jl("unknowns/setup_unknown_queue.jsonl"); assert {x["setup_id"] for x in inv}<={x.get("setup_id") for x in q}
