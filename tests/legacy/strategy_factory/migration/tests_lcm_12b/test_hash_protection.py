from src.engine.tooling.strategy_factory.lcm.lcm_12b.io import load_json,iter_jsonl
def test_hash_protected_paths_remain_active_compatibility(reconciliation_root):
    reg=load_json(reconciliation_root/"documentation_redirect_registry.json")
    rows=list(iter_jsonl(reconciliation_root/reg["redirect_records_path"]))
    deferred=[r for r in rows if r["materialization_status"]=="DEFERRED_HASH_PROTECTED"]
    assert len(deferred)==reg["deferred_hash_protected_count"]
    assert all(r["compatibility_status"]=="ACTIVE_COMPATIBILITY_HASH_PROTECTED" for r in deferred)
