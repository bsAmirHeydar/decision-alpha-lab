import pytest
from fp_i13_release import *
def test_incremental_no_full_scan(fixture,instance): assert run_incremental(fixture,instance,chunk_size=7).telemetry.full_scan_count==0
def test_incremental_chunk_count(fixture,instance):
 r=run_incremental(fixture,instance,chunk_size=10);assert r.telemetry.chunk_count==12
def test_incremental_inventory_stable_across_chunk_sizes(fixture,instance): assert run_incremental(fixture,instance,chunk_size=1).inventory.inventory_hash==run_incremental(fixture,instance,chunk_size=31).inventory.inventory_hash
def test_invalid_chunk_rejected(fixture,instance):
 with pytest.raises(Exception):run_incremental(fixture,instance,chunk_size=0)
def test_telemetry_positive(fixture,instance):
 t=run_incremental(fixture,instance).telemetry;assert t.elapsed_ns>0 and t.peak_memory_bytes>=0 and t.events_per_second>0
