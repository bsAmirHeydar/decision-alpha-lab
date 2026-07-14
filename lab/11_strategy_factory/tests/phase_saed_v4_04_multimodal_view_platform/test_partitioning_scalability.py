from saed_v4_multimodal_views.partitioning import shard_key,cache_key

def test_shard_key_deterministic():assert shard_key('t','price','2026-01-01T00:00:00Z')==shard_key('t','price','2026-01-01T12:00:00Z')
def test_shard_key_bounded():assert all(0<=shard_key(f't{i}','price','2026-01-01T00:00:00Z',17)<17 for i in range(100))
def test_cache_key_source_order_independent():assert cache_key('a','k','e','development',['1','2'])==cache_key('a','k','e','development',['2','1'])
