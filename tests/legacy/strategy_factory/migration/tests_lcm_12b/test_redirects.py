from tools.strategy_factory.lcm.lcm_12b.io import load_json,iter_jsonl
def test_redirects_are_loop_free_and_targets_exist(repo_root,reconciliation_root):
    reg=load_json(reconciliation_root/"documentation_redirect_registry.json")
    rows=list(iter_jsonl(reconciliation_root/reg["redirect_records_path"]))
    assert len(rows)==reg["redirect_requirement_count"]
    assert reg["redirect_loop_count"]==0 and reg["missing_target_count"]==0
    assert all(r["legacy_path"]!=r["canonical_target_path"] and (repo_root/r["canonical_target_path"]).exists() for r in rows)
