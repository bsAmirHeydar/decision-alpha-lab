from fp_i13_release import *
def test_full_incremental_parity(fixture,instance): assert compare_runs(run_full(fixture,instance),run_incremental(fixture,instance,chunk_size=9)).status==ParityStatus.PASS
def test_event_chain_matches(fixture,instance): assert run_full(fixture,instance).inventory.event_chain_hash==run_incremental(fixture,instance,chunk_size=11).inventory.event_chain_hash
def test_visual_inventory_matches(fixture,instance): assert run_full(fixture,instance).inventory.visual_object_ids==run_incremental(fixture,instance,chunk_size=4).inventory.visual_object_ids
def test_alert_inventory_matches(fixture,instance): assert run_full(fixture,instance).inventory.alert_ids==run_incremental(fixture,instance).inventory.alert_ids
