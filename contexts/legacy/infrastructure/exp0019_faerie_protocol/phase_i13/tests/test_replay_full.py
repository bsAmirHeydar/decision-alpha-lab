from fp_i13_release import *
def test_full_replay_builds_inventory(fixture,instance):
 r=run_full(fixture,instance);assert len(r.inventory.semantic_ids)==28;assert len(r.inventory.visual_object_ids)==28
def test_historical_alerts_suppressed(fixture,instance):
 r=run_full(fixture,instance);assert len(r.inventory.suppressed_historical_alert_ids)==14;assert len(r.inventory.alert_ids)==14
def test_exports_preserved(fixture,instance): assert len(run_full(fixture,instance).inventory.export_ids)==28
def test_full_scan_counter_is_one(fixture,instance): assert run_full(fixture,instance).telemetry.full_scan_count==1
def test_repeated_full_inventory_stable(fixture,instance): assert run_full(fixture,instance).inventory.inventory_hash==run_full(fixture,instance).inventory.inventory_hash
