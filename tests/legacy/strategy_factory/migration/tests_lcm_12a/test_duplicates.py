def test_exact_duplicate_groups_have_hash_proof(load):
    reg=load("documentation_duplicate_registry.json")
    assert all(x["proof"]=="IDENTICAL_SHA256_BYTES" and x["member_count"]>=2 for x in reg["byte_duplicate_groups"])
def test_normalized_duplicate_groups_are_not_byte_only(load):
    reg=load("documentation_duplicate_registry.json")
    assert all(x["proof"]=="IDENTICAL_NORMALIZED_SHA256" for x in reg["normalized_duplicate_groups"])
