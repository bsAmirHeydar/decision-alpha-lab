from src.engine.tooling.strategy_factory.lcm.lcm_12b.io import load_json,iter_jsonl
def test_all_approved_targets_and_legacy_paths_exist(repo_root,reconciliation_root):
    manifest=load_json(reconciliation_root/"documentation_move_manifest.json")
    rows=list(iter_jsonl(reconciliation_root/manifest["move_records_path"]))
    assert manifest["approved_candidate_count"] == manifest["target_materialized_count"] == len(rows) == 656
    assert manifest["source_delete_count"] == 0
    assert all((repo_root/r["source_path"]).exists() and (repo_root/r["target_path"]).exists() for r in rows)
