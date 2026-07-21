from .conftest import j,jl
def test_outputs_do_not_claim_source_change_or_cutover():
 h=j("handoff/lcm10b_to_lcm10c_handoff.json");assert not h["source_move_allowed"] and not h["source_delete_allowed"] and not h["consumer_cutover_allowed"];assert all(not x["consumer_cutover_allowed"] for x in jl("compatibility/legacy_execution_adapter_registry.jsonl"))
