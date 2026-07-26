from src.engine.tooling.strategy_factory.lcm.lcm_12b.io import load_json,iter_jsonl
def test_rewritten_links_have_existing_destinations(reconciliation_root):
    report=load_json(reconciliation_root/"obsidian_link_report.json")
    rows=list(iter_jsonl(reconciliation_root/"records/documentation_link_rewrite_records.jsonl"))
    assert report["new_broken_reference_count"]==0
    assert report["canonical_basename_collision_count"]==0
    assert all(r["destination_exists"] and r["validation_status"]=="PASS" for r in rows)
