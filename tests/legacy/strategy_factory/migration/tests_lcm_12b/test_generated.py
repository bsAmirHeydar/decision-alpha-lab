from src.engine.tooling.strategy_factory.lcm.lcm_12b.io import load_json,iter_jsonl
def test_generated_documents_are_source_and_producer_bound(reconciliation_root):
    reg=load_json(reconciliation_root/"generated_document_registry.json")
    rows=list(iter_jsonl(reconciliation_root/reg["records_path"]))
    assert len(rows)==reg["generated_document_count"]
    assert reg["all_generated_documents_source_bound"] and reg["all_generated_documents_producer_bound"]
    assert all(not r["hand_edit_allowed"] and not r["canonical_authority_allowed"] for r in rows)
