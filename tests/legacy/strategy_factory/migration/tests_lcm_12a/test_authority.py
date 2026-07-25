from tools.strategy_factory.lcm.lcm_12a.io import load_jsonl
def test_every_active_document_classified(mapping_root,load):
    reg=load("documentation_authority_registry.json")
    rows=load_jsonl(mapping_root/reg["records_path"])
    allowed={"CANONICAL","SUPPORTING_EVIDENCE","GENERATED_PROJECTION","SUPERSEDED","DUPLICATE","CONTRADICTORY","ARCHIVE_ONLY","UNKNOWN"}
    assert len(rows)==reg["document_count"]
    assert all(r["authority"]["authority_class"] in allowed for r in rows if r["active"])
def test_generated_projection_not_auto_canonical(mapping_root,load):
    reg=load("documentation_authority_registry.json")
    rows=load_jsonl(mapping_root/reg["records_path"])
    assert not any("/generated/" in ("/"+r["path"].lower()) and r["authority"]["authority_class"]=="CANONICAL" for r in rows)
