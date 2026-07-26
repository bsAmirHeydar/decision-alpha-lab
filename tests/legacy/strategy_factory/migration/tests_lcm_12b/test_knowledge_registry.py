from src.engine.tooling.strategy_factory.lcm.lcm_12b.io import load_json,iter_jsonl
def test_canonical_knowledge_registry_is_complete(repo_root,reconciliation_root):
    reg=load_json(reconciliation_root/"canonical_knowledge_registry.json")
    rows=list(iter_jsonl(reconciliation_root/reg["records_path"]))
    assert len(rows)==reg["knowledge_record_count"]==25965
    assert (repo_root/reg["canonical_moc_path"]).is_file()
    assert (repo_root/reg["generated_moc_path"]).is_file()
