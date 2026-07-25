from tools.strategy_factory.lcm.lcm_12a.io import load_jsonl
def test_unknown_queue_is_explicit_and_scoped(mapping_root,load):
    q=load("documentation_unknown_queue.json")
    rows=load_jsonl(mapping_root/q["unknowns_path"])
    assert len(rows)==q["unknown_count"]
    assert q["unknowns_block_affected_paths_only"] is True
    assert q["global_waiver_allowed"] is False
