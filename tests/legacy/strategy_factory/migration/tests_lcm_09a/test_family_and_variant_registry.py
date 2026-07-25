from .conftest import j,jl
def test_family_grouping_never_claims_equivalence():
 f=j("families/setup_family_registry.json"); assert f["family_count"]==6; assert all(not x["semantic_equivalence_claimed"] and not x["merge_authorized"] for x in f["families"])
def test_variants_complete_and_explicit():
 v=jl("variants/setup_variant_registry.jsonl"); assert len(v)==60; assert all("direction_variants" in x and "timeframe_tokens" in x and not x["semantic_equivalence_claimed"] for x in v)
