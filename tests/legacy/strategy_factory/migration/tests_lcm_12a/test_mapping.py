def test_canonical_mappings_are_total(load):
    mapping=load("documentation_canonical_map.json")
    authority=load("documentation_authority_registry.json")
    assert mapping["mapping_count"]==authority["document_count"]
    assert all(m["canonical_document_id"] and m["source_digest"].startswith("sha256:") for m in mapping["mappings"])
def test_no_target_collisions(load):
    assert load("documentation_canonical_map.json")["target_collisions"]==[]
